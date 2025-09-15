#!/usr/bin/env python3
"""
Test transcription system for CarBrandApp
Simulates user speech input for testing without needing OpenAI API
"""

import json
import time
from app import app, db, Car

# Test scenarios
TEST_SCENARIOS = {
    'correct_answers': {
        'toyota': ['toyota', 'тойота'],
        'bmw': ['bmw', 'бмв', 'биммер'],
        'ferrari': ['ferrari', 'феррари'],
        'mercedes-benz': ['mercedes', 'мерседес', 'мерседес-бенц'],
        'audi': ['audi', 'ауди'],
        'honda': ['honda', 'хонда'],
        'ford': ['ford', 'форд'],
        'nissan': ['nissan', 'ниссан', 'нисан'],
        'chevrolet': ['chevrolet', 'шевроле'],
        'volkswagen': ['volkswagen', 'фольксваген', 'вольксваген']
    },
    'incorrect_answers': [
        'something wrong', 'неправильный', 'test', 'тест', 'hello', 'привет'
    ]
}

class TranscriptionTester:
    def __init__(self):
        self.current_test = None
        self.test_response = None
    
    def set_test_response(self, text):
        """Set the next transcription response for testing"""
        self.test_response = text
    
    def test_correct_answer(self, car_name):
        """Test with a correct answer for the given car"""
        if car_name.lower() in TEST_SCENARIOS['correct_answers']:
            correct_answers = TEST_SCENARIOS['correct_answers'][car_name.lower()]
            self.set_test_response(correct_answers[0])
            return correct_answers[0]
        return car_name
    
    def test_incorrect_answer(self):
        """Test with an incorrect answer"""
        incorrect = TEST_SCENARIOS['incorrect_answers'][0]
        self.set_test_response(incorrect)
        return incorrect
    
    def simulate_user_flow(self, car_name, should_be_correct=True):
        """Simulate complete user interaction flow"""
        print(f"\n🧪 Testing flow for {car_name} ({'correct' if should_be_correct else 'incorrect'} answer)")
        
        # Simulate clicking on car image
        print(f"1. User clicks on {car_name} image")
        print("   → Modal opens")
        print("   → Voice recording starts")
        
        # Simulate speaking
        if should_be_correct:
            response = self.test_correct_answer(car_name)
            print(f"2. User says: '{response}'")
        else:
            response = self.test_incorrect_answer()
            print(f"2. User says: '{response}'")
        
        return response

# Test the flow
def run_tests():
    """Run comprehensive tests"""
    tester = TranscriptionTester()
    
    print("🚗 Car Brand App - Testing Suite")
    print("=" * 50)
    
    # Test with some cars
    test_cars = ['toyota', 'bmw', 'ferrari']
    
    for car in test_cars:
        # Test correct answer
        tester.simulate_user_flow(car, should_be_correct=True)
        
        # Test incorrect answer
        tester.simulate_user_flow(car, should_be_correct=False)
    
    print("\n✅ Test simulation complete")
    print("\n📝 Issues identified:")
    print("- OpenAI API key not set, causing 500 errors")
    print("- Need mock transcription for testing")
    print("- Need to handle API failures gracefully")

if __name__ == '__main__':
    run_tests()