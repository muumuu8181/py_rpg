"""
Working example of RPG game automation with Selenium
This demonstrates the most reliable method for controlling the game
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def automate_rpg_game():
    # Setup driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    
    try:
        # Load game
        driver.get("file:///C:/Users/user/Desktop/work/90_cc/20250910/minimal-rpg-game/custom_bg_game.html")
        
        # Wait for game to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gameCanvas"))
        )
        
        # Wait for game initialization
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return typeof game !== 'undefined' && game.frameCount > 0")
        )
        
        print("Game loaded successfully!")
        time.sleep(1)
        
        # Get initial position
        pos = driver.execute_script("return {x: game.player.x, y: game.player.y}")
        print(f"Starting position: X={pos['x']}, Y={pos['y']}")
        
        # SOLUTION: Direct manipulation of game.keys object
        # This is the most reliable method for canvas-based games
        
        print("\nMoving player...")
        
        # Move RIGHT
        print("Moving right...")
        driver.execute_script("""
            game.keys['d'] = true;
            game.keys['D'] = true;
            game.keys['ArrowRight'] = true;
        """)
        time.sleep(1)  # Move for 1 second
        driver.execute_script("""
            game.keys['d'] = false;
            game.keys['D'] = false;
            game.keys['ArrowRight'] = false;
        """)
        
        # Move DOWN
        print("Moving down...")
        driver.execute_script("""
            game.keys['s'] = true;
            game.keys['S'] = true;
            game.keys['ArrowDown'] = true;
        """)
        time.sleep(1)
        driver.execute_script("""
            game.keys['s'] = false;
            game.keys['S'] = false;
            game.keys['ArrowDown'] = false;
        """)
        
        # Move LEFT
        print("Moving left...")
        driver.execute_script("""
            game.keys['a'] = true;
            game.keys['A'] = true;
            game.keys['ArrowLeft'] = true;
        """)
        time.sleep(1)
        driver.execute_script("""
            game.keys['a'] = false;
            game.keys['A'] = false;
            game.keys['ArrowLeft'] = false;
        """)
        
        # Move UP
        print("Moving up...")
        driver.execute_script("""
            game.keys['w'] = true;
            game.keys['W'] = true;
            game.keys['ArrowUp'] = true;
        """)
        time.sleep(1)
        driver.execute_script("""
            game.keys['w'] = false;
            game.keys['W'] = false;
            game.keys['ArrowUp'] = false;
        """)
        
        # Get final position
        pos = driver.execute_script("return {x: game.player.x, y: game.player.y}")
        print(f"\nFinal position: X={pos['x']}, Y={pos['y']}")
        
        # Demonstrate attack
        print("\nFiring projectiles...")
        for i in range(3):
            driver.execute_script("playerAttack();")
            time.sleep(0.5)
        
        # Demonstrate special attack
        print("Executing special attack...")
        driver.execute_script("""
            game.player.mp = game.player.maxMp;  // Ensure enough MP
            specialAttack();
        """)
        
        print("\n✅ Automation successful!")
        print("\nPress Enter to close...")
        input()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

def create_movement_function():
    """
    Example function you can use in your automation scripts
    """
    def move_player(driver, direction, duration=0.5):
        """
        Move player in specified direction
        
        Args:
            driver: Selenium webdriver instance
            direction: 'up', 'down', 'left', 'right'
            duration: How long to move (in seconds)
        """
        key_mappings = {
            'up': ['w', 'W', 'ArrowUp'],
            'down': ['s', 'S', 'ArrowDown'],
            'left': ['a', 'A', 'ArrowLeft'],
            'right': ['d', 'D', 'ArrowRight']
        }
        
        if direction not in key_mappings:
            raise ValueError(f"Invalid direction: {direction}")
        
        keys = key_mappings[direction]
        
        # Start movement
        for key in keys:
            driver.execute_script(f"game.keys['{key}'] = true;")
        
        time.sleep(duration)
        
        # Stop movement
        for key in keys:
            driver.execute_script(f"game.keys['{key}'] = false;")
    
    return move_player

if __name__ == "__main__":
    # Run the automation example
    automate_rpg_game()
    
    # Example of how to use the movement function:
    """
    driver = webdriver.Chrome()
    move = create_movement_function()
    
    # Move player around
    move(driver, 'right', 1.0)  # Move right for 1 second
    move(driver, 'down', 0.5)   # Move down for 0.5 seconds
    move(driver, 'left', 1.0)   # Move left for 1 second
    move(driver, 'up', 0.5)     # Move up for 0.5 seconds
    """