"""Conformance tests and synthetic oracle; never reads corpus or writes a sample.
Run from docs/airtable: python3 -m unittest discover -s tests -v
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import unittest

DOCS = Path(__file__).resolve().parents[1]
TEMPLATE = DOCS / 'sampling-manifest.template.json'


def allocation(sizes):
    """Synthetic oracle of the documented bounded allocation, not a pilot CLI."""
    sizes = {h: n for h, n in sizes.items() if n >= 3}
    if len(sizes) == 6 and min(sizes.values()) >= 5:
        return {h: 5 for h in sizes}
    total = next((t for t in [30, 29, 31, 28, 27, 26, 25, 24]
                  if 3 * len(sizes) <= t <= sum(min(6, n) for n in sizes.values())), None)
    if total is None:
        raise ValueError('NO_FEASIBLE_TOTAL')
    allocated = dict.fromkeys(sizes, 3)
    while sum(allocated.values()) < total:
        h = min((h for h in sizes if allocated[h] < min(6, sizes[h])),
                key=lambda h: (-(Fraction(total * sizes[h], sum(sizes.values())) - allocated[h]), h))
        allocated[h] += 1
    return allocated


def payload(seed, stratum, item):
    if any(not x or x != x.strip() or '\x1f' in x for x in (seed, stratum, item)):
        raise ValueError('INVALID_HASH_COMPONENT')
    return b'\x1f'.join(x.encode('utf-8') for x in (seed, stratum, item))


def order(ids, stratum, digest=None):
    if len(set(ids)) != len(ids):
        raise ValueError('DUPLICATE_ID')
    digest = digest or (lambda b: hashlib.sha256(b).hexdigest())
    return sorted(ids, key=lambda i: (digest(payload('cv-pilot-0.1', stratum, i)), i))


class ContractTests(unittest.TestCase):
    def setUp(self):
        path = TEMPLATE if TEMPLATE.exists() else DOCS.parents[1] / 'data/public/airtable/manifest.template.json'
        self.sampling = json.loads(path.read_text())['sampling']

    def test_json_separator_is_one_byte(self):
        rule = self.sampling['randomization']
        if isinstance(rule, str):
            self.assertIn('\x1f', rule)  # reproduces the original escaped-literal defect
        else:
            self.assertEqual(rule['separator'].encode('utf-8'), b'\x1f')

    def test_template_payload_matches_fixed_digest(self):
        rule = self.sampling['randomization']
        components = {'sampling_seed': 'cv-pilot-0.1', 'stratum': 'moeda', 'canonical_item_id': 'BR-001'}
        raw = rule['separator'].join(components[k] for k in rule['component_order']).encode(rule['encoding'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), '0eaba708d95bfdb39eb74d8af7d745dcb149b2712a84c64b0f72f9a727996f27')
        self.assertFalse(rule['bom'])
        self.assertFalse(rule['trailing_newline'])

    def test_order_is_explicit(self):
        self.assertEqual(self.sampling.get('hash_sort'), ['sha256_hex:asc', 'canonical_item_id:unicode_scalar_asc'])

    def test_unapproved_frame_blocks_execution(self):
        self.assertEqual(self.sampling.get('status'), 'blocked_pending_frame')
        self.assertIsNone(self.sampling['frame_specification']['eligibility_policy'])
        self.assertIsNone(self.sampling['actual_size'])

    def test_identity_and_eligibility_are_required(self):
        self.assertTrue({'ID do corpus', 'source_row_id', 'eligibility_status'} <= set(self.sampling['required_frame_fields']))

    def test_protocol_anchor_exists(self):
        self.assertEqual(self.sampling['protocol'], 'docs/airtable/qa-protocol.md#amostragem-pré-registrada-do-piloto-de-visão-computacional')

    def test_documented_vectors(self):
        vectors = [('moeda', 'BR-001', '63762d70696c6f742d302e311f6d6f6564611f42522d303031', '0eaba708d95bfdb39eb74d8af7d745dcb149b2712a84c64b0f72f9a727996f27'),
                   ('pintura', 'Á-01', '63762d70696c6f742d302e311f70696e747572611fc3812d3031', '4eab12fe49fb87fdb0ada81ad954bb272dd128232796c3ac01ca9c7391d2b45b')]
        for h, i, hex_bytes, digest in vectors:
            with self.subTest(item=i):
                b = payload('cv-pilot-0.1', h, i)
                self.assertEqual(b.hex(), hex_bytes)
                self.assertEqual(hashlib.sha256(b).hexdigest(), digest)
                self.assertIn(digest, (DOCS / 'qa-protocol.md').read_text())

    def test_order_reserves_and_input_permutation(self):
        ids = ['BR-003', 'BR-001', 'BR-002', 'BR-004']
        ranked = order(ids, 'moeda')
        self.assertEqual(ranked, order(list(reversed(ids)), 'moeda'))
        self.assertEqual(ranked, ['BR-001', 'BR-003', 'BR-004', 'BR-002'])
        selected, reserves = ranked[:3], dict(zip(ranked[3:], range(1, len(ranked) - 2)))
        self.assertFalse(set(selected) & reserves.keys())
        self.assertEqual(reserves, {'BR-002': 1})

    def test_hash_tie_uses_unicode_id(self):
        self.assertEqual(order(['á', 'B', 'a'], 'pintura', lambda _: '0' * 64), ['B', 'a', 'á'])

    def test_invalid_ids_block(self):
        for ids in [['A', 'A'], [''], [' A'], ['A\x1fB']]:
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                order(ids, 'moeda')

    def test_balanced_six_by_five(self):
        self.assertEqual(allocation(dict(zip('abcdef', [5, 6, 7, 8, 9, 10]))), dict.fromkeys('abcdef', 5))

    def test_small_stratum_uses_bounded_fallback(self):
        self.assertEqual(allocation(dict(zip('abcdef', [3, 5, 5, 5, 5, 7]))), dict(zip('abcdef', [3, 5, 5, 5, 5, 6])))

    def test_small_strata_are_not_allocated(self):
        result = allocation(dict(zip('abcdefxy', [6]*6 + [1, 2])))
        self.assertEqual(result, dict.fromkeys('abcdef', 5))
        self.assertIn('inclusive 1 e 2', (DOCS / 'schema.md').read_text())

    def test_fallback_priority_and_no_feasible_total(self):
        self.assertEqual(sum(allocation(dict(zip('abcde', [5, 6, 6, 6, 6]))).values()), 29)
        self.assertEqual(sum(allocation(dict.fromkeys('abcd', 6)).values()), 24)
        for sizes in [{}, {'a': 2}, dict.fromkeys('abc', 6), dict.fromkeys('abcdefghijk', 6)]:
            with self.subTest(sizes=sizes), self.assertRaises(ValueError):
                allocation(sizes)

    def test_allocation_independent_of_dictionary_order(self):
        sizes = dict.fromkeys('abcdefg', 10)
        self.assertEqual(allocation(sizes), dict(zip('abcdefg', [5, 5, 4, 4, 4, 4, 4])))
        self.assertEqual(allocation(sizes), allocation(dict(reversed(list(sizes.items())))))


if __name__ == '__main__':
    unittest.main()
