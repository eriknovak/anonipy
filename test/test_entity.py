import unittest

from anonipy.definitions import Entity


# =====================================
# Test Entity
# =====================================


class TestEntity(unittest.TestCase):

    def test_init_default(self):
        entity = Entity(
            text="test",
            label="test",
            start_index=0,
            end_index=4,
        )
        self.assertEqual(entity.text, "test")
        self.assertEqual(entity.label, "test")
        self.assertEqual(entity.start_index, 0)
        self.assertEqual(entity.end_index, 4)
        self.assertEqual(entity.score, 1.0)
        self.assertEqual(entity.type, None)
        self.assertEqual(entity.regex, ".*")

    def test_init_custom(self):
        entity = Entity(
            text="test",
            label="test",
            start_index=0,
            end_index=4,
            score=0.89,
            type="test",
            regex="test",
        )
        self.assertEqual(entity.text, "test")
        self.assertEqual(entity.label, "test")
        self.assertEqual(entity.start_index, 0)
        self.assertEqual(entity.end_index, 4)
        self.assertEqual(entity.score, 0.89)
        self.assertEqual(entity.type, "test")
        self.assertEqual(entity.regex, "test")


if __name__ == "__main__":
    unittest.main()
