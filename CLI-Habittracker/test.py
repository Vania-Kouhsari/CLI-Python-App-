import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from analysis import calculate_streak, calculate_longest_streak
import main
import database

class TestHabitTracker(unittest.TestCase):

    # Tests calculate_streak() for a daily habit with 5 consecutive completions.
    def test_calculate_streak_daily(self):
        today = datetime.now().date()
        completions = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
        result = calculate_streak(1, 'daily', completions)
        self.assertEqual(result, 5)

    # Tests calculate_streak() for a weekly habit with 3 consecutive weeks completed.
    def test_calculate_streak_weekly(self):
        today = datetime.now().date()
        completions = [(today - timedelta(weeks=i)).strftime("%Y-%m-%d") for i in range(3)]
        result = calculate_streak(1, 'weekly', completions)
        self.assertEqual(result, 3)

    # Tests calculate_streak() when there are no completions.
    def test_calculate_streak_empty(self):
        result = calculate_streak(1, 'daily', [])
        self.assertEqual(result, 0)

    # Tests calculate_longest_streak() for a streak without interruptions.
    def test_longest_streak_daily(self):
        today = datetime.now().date()
        completions = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
        result = calculate_longest_streak(completions, 'daily')
        self.assertEqual(result, 3)

    # Tests calculate_longest_streak() when there is a gap in the streak.
    def test_longest_streak_with_gap(self):
        today = datetime.now().date()
        completions = [
            (today - timedelta(days=0)).strftime("%Y-%m-%d"),
            (today - timedelta(days=1)).strftime("%Y-%m-%d"),
            (today - timedelta(days=3)).strftime("%Y-%m-%d"),  # gap here
        ]
        result = calculate_longest_streak(completions, 'daily')
        self.assertEqual(result, 2)

    # Tests the create_habit() flow when a new, valid habit is added.
    @patch('main.get_connection')
    @patch('builtins.input', side_effect=["Test Habit", "Test Description", "daily"])
    def test_create_habit_success(self, mock_input, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  

        with patch('main.Habit', autospec=True) as mock_habit, patch('main.post_action_menu'), patch('time.sleep'):
            mock_instance = mock_habit.return_value
            mock_instance.name = "Test Habit"
            mock_instance.description = "Test Description"
            mock_instance.periodicity = "daily"
            mock_instance.creation_time = "2025-08-01"

            main.create_habit()
            self.assertTrue(mock_cursor.execute.called)
            self.assertTrue(mock_conn.return_value.commit.called)

    # ests deletion of a habit when selected by index.
    @patch('main.get_connection')
    @patch('builtins.input', side_effect=["1"])
    def test_delete_habit_by_index(self, mock_input, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, "Habit 1")]

        with patch('main.post_action_menu'), patch('time.sleep'):
            main.delete_habit()
            mock_cursor.execute.assert_any_call("DELETE FROM habits WHERE id = ?", (1,))

    # Tests marking a habit as completed for today, when not already marked.
    @patch('main.get_connection')
    @patch('builtins.input', side_effect=["1"])
    def test_mark_completed_new_day(self, mock_input, mock_conn):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, "Habit 1")]
        mock_cursor.fetchone.return_value = None  

        with patch('main.post_action_menu'), patch('time.sleep'):
            main.mark_completed()
            self.assertTrue(mock_cursor.execute.called)
            self.assertTrue(mock_conn.return_value.commit.called)


if __name__ == "__main__":
    unittest.main()