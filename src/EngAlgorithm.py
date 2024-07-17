import random
import Levenshtein  # Importing the Levenshtein package

verbs = [
    "jump", "run", "eat", "sleep", "laugh", "cry", "sing", "dance", "swim", 
    "write", "read", "think", "talk", "listen", "cook", "play", "work", 
    "study", "draw", "paint", "climb", "drive", "fly", "fight", "travel", 
    "build", "clean", "wash", "fix", "cut", "grow", "plant", "drive", 
    "push", "pull", "throw", "catch", "kick", "punch", "shoot", "stab", 
    "save", "spend", "earn", "sell", "buy", "teach", "learn", "program"
]

def choose_word():
    return random.choice(verbs) #choosing a random word from the list of verbs in "verbs" array

def calculate_score(guess, word): 
    # Calculate Lenovenshtein distance between guess and word
    distance = Levenshtein.distance(guess, word) #.distance will calculate the distance between each letter in the strings and how much modification would've needed
    #the amount of modification needed to reach the correct string
    
    # Convert Levenshtein distance to a score out of 1000, ensuring a minimum score of 100
    max_distance = max(len(guess), len(word))  # Maximum possible distance, meaning the length of the word

    score = max(100, (max_distance - distance) / max_distance * 1000) #calculation
    
    return score

def main():
    print("Welcome to the Verb Guessing Game!")
    while True:
        chosen_word = choose_word()
        print(f"\nGuess the verb! (Hint: It's related to actions)")
        
        while True:
            user_guess = input("Your guess (or type 'give up' to see the answer): ").strip().lower()
            
            if user_guess == "give up":
                print(f"\nYou gave up! The correct word was: {chosen_word}")
                break
            elif user_guess == chosen_word:
                score = 1000  # If the guess is correct, the score is 1000
                print("\nCongratulations! You guessed it right!")
                print(f"Score: {score}/1000")
                break
            else:
                score = calculate_score(user_guess, chosen_word)
                print(f"Score: {score:.2f}/1000")
        
        play_again = input("\nPlay again? (yes/no): ").strip().lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
