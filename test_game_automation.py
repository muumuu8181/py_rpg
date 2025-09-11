"""
Focused test script for RPG game automation
Addresses common canvas game automation issues
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=3')  # Suppress logs
    return webdriver.Chrome(options=options)

def wait_for_game_ready(driver):
    """Wait for game to be fully initialized"""
    # Wait for canvas
    canvas = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "gameCanvas"))
    )
    
    # Wait for game object to exist
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return typeof game !== 'undefined' && game.frameCount > 0")
    )
    
    print("✅ Game is ready")
    return canvas

def get_player_info(driver):
    """Get player position and state"""
    return driver.execute_script("""
        if (typeof game !== 'undefined' && game.player) {
            return {
                x: Math.round(game.player.x),
                y: Math.round(game.player.y),
                facing: game.player.facing,
                hp: game.player.hp,
                score: game.player.score
            };
        }
        return null;
    """)

def move_player_solution_1(driver):
    """Solution 1: Direct key state manipulation with proper timing"""
    print("\n🔧 Solution 1: Direct key state manipulation")
    
    initial = get_player_info(driver)
    print(f"Initial position: X:{initial['x']}, Y:{initial['y']}")
    
    # Move right for 500ms
    driver.execute_script("""
        // Start moving right
        game.keys['d'] = true;
        game.keys['D'] = true;
        game.keys['ArrowRight'] = true;
    """)
    
    time.sleep(0.5)  # Let movement happen
    
    # Stop moving right
    driver.execute_script("""
        game.keys['d'] = false;
        game.keys['D'] = false;
        game.keys['ArrowRight'] = false;
    """)
    
    # Move down for 500ms
    driver.execute_script("""
        game.keys['s'] = true;
        game.keys['S'] = true;
        game.keys['ArrowDown'] = true;
    """)
    
    time.sleep(0.5)
    
    # Stop all movement
    driver.execute_script("""
        game.keys['s'] = false;
        game.keys['S'] = false;
        game.keys['ArrowDown'] = false;
    """)
    
    final = get_player_info(driver)
    print(f"Final position: X:{final['x']}, Y:{final['y']}")
    
    if initial['x'] != final['x'] or initial['y'] != final['y']:
        print("✅ Movement successful!")
        return True
    else:
        print("❌ No movement detected")
        return False

def move_player_solution_2(driver, canvas):
    """Solution 2: Synthetic events with proper event properties"""
    print("\n🔧 Solution 2: Synthetic keyboard events")
    
    initial = get_player_info(driver)
    print(f"Initial position: X:{initial['x']}, Y:{initial['y']}")
    
    # Focus the canvas first
    driver.execute_script("arguments[0].focus();", canvas)
    
    # Dispatch proper keyboard events
    driver.execute_script("""
        function sendKey(key, keyCode, type) {
            const event = new KeyboardEvent(type, {
                key: key,
                keyCode: keyCode,
                code: 'Key' + key.toUpperCase(),
                which: keyCode,
                bubbles: true,
                cancelable: true,
                view: window
            });
            document.dispatchEvent(event);
            window.dispatchEvent(event);
            document.activeElement.dispatchEvent(event);
        }
        
        // Move right
        sendKey('d', 68, 'keydown');
    """)
    
    time.sleep(0.5)
    
    driver.execute_script("sendKey('d', 68, 'keyup');")
    
    # Move down
    driver.execute_script("""
        sendKey('s', 83, 'keydown');
    """)
    
    time.sleep(0.5)
    
    driver.execute_script("sendKey('s', 83, 'keyup');")
    
    final = get_player_info(driver)
    print(f"Final position: X:{final['x']}, Y:{final['y']}")
    
    if initial['x'] != final['x'] or initial['y'] != final['y']:
        print("✅ Movement successful!")
        return True
    else:
        print("❌ No movement detected")
        return False

def move_player_solution_3(driver):
    """Solution 3: Override the event listener temporarily"""
    print("\n🔧 Solution 3: Temporary event listener override")
    
    initial = get_player_info(driver)
    print(f"Initial position: X:{initial['x']}, Y:{initial['y']}")
    
    # Store original listeners and create controlled movement
    driver.execute_script("""
        // Create a movement sequence
        const movements = [
            { keys: ['d', 'D', 'ArrowRight'], duration: 500 },
            { keys: ['s', 'S', 'ArrowDown'], duration: 500 }
        ];
        
        let moveIndex = 0;
        
        function executeMovement() {
            if (moveIndex < movements.length) {
                const move = movements[moveIndex];
                
                // Set keys to true
                move.keys.forEach(key => game.keys[key] = true);
                
                setTimeout(() => {
                    // Set keys to false
                    move.keys.forEach(key => game.keys[key] = false);
                    moveIndex++;
                    executeMovement();
                }, move.duration);
            }
        }
        
        executeMovement();
    """)
    
    time.sleep(1.5)  # Wait for movements to complete
    
    final = get_player_info(driver)
    print(f"Final position: X:{final['x']}, Y:{final['y']}")
    
    if initial['x'] != final['x'] or initial['y'] != final['y']:
        print("✅ Movement successful!")
        return True
    else:
        print("❌ No movement detected")
        return False

def test_game_controls(driver, canvas):
    """Test all game controls including movement and attacks"""
    print("\n🎮 Testing full game controls")
    
    # Test attack
    initial_score = get_player_info(driver)['score']
    
    # Fire projectile
    driver.execute_script("""
        // Simulate space key for attack
        game.keys[' '] = true;
        playerAttack();
        game.keys[' '] = false;
    """)
    
    print("✅ Attack fired")
    
    # Test special attack
    driver.execute_script("""
        // Make sure we have enough MP
        game.player.mp = game.player.maxMp;
        
        // Trigger special attack
        game.keys['e'] = true;
        specialAttack();
        game.keys['e'] = false;
    """)
    
    print("✅ Special attack fired")
    
    # Create a simple movement pattern
    print("\n🎯 Executing movement pattern...")
    driver.execute_script("""
        const pattern = [
            { dir: 'right', keys: ['d', 'D'], time: 300 },
            { dir: 'down', keys: ['s', 'S'], time: 300 },
            { dir: 'left', keys: ['a', 'A'], time: 300 },
            { dir: 'up', keys: ['w', 'W'], time: 300 }
        ];
        
        let index = 0;
        
        function moveNext() {
            if (index < pattern.length) {
                const move = pattern[index];
                console.log('Moving ' + move.dir);
                
                // Start movement
                move.keys.forEach(k => game.keys[k] = true);
                
                setTimeout(() => {
                    // Stop movement
                    move.keys.forEach(k => game.keys[k] = false);
                    index++;
                    
                    setTimeout(moveNext, 100);
                }, move.time);
            }
        }
        
        moveNext();
    """)
    
    time.sleep(1.5)
    print("✅ Movement pattern completed")

def main():
    """Main test function"""
    print("🎮 RPG Game Automation Test")
    print("=" * 50)
    
    driver = setup_driver()
    
    try:
        # Load game
        game_url = "file:///C:/Users/user/Desktop/work/90_cc/20250910/minimal-rpg-game/custom_bg_game.html"
        print(f"Loading game: {game_url}")
        driver.get(game_url)
        
        # Wait for game initialization
        canvas = wait_for_game_ready(driver)
        time.sleep(1)  # Extra time for stability
        
        # Run solutions
        solutions_success = []
        
        # Test Solution 1
        if move_player_solution_1(driver):
            solutions_success.append("Solution 1: Direct key manipulation")
        
        # Reset position
        driver.execute_script("game.player.x = 400; game.player.y = 300;")
        time.sleep(0.5)
        
        # Test Solution 2
        if move_player_solution_2(driver, canvas):
            solutions_success.append("Solution 2: Synthetic events")
        
        # Reset position
        driver.execute_script("game.player.x = 400; game.player.y = 300;")
        time.sleep(0.5)
        
        # Test Solution 3
        if move_player_solution_3(driver):
            solutions_success.append("Solution 3: Event override")
        
        # Test full controls
        test_game_controls(driver, canvas)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 SUMMARY")
        print("=" * 50)
        
        if solutions_success:
            print("✅ Working solutions:")
            for solution in solutions_success:
                print(f"  - {solution}")
            
            print("\n💡 Recommendation: Use Solution 1 (Direct key manipulation)")
            print("   It's the most reliable and straightforward approach.")
        else:
            print("❌ No solutions worked. The game might have additional")
            print("   security measures or require different approach.")
        
        print("\n🔍 For your automation, use this pattern:")
        print("""
# Move right
driver.execute_script("game.keys['d'] = true;")
time.sleep(0.5)  # Move duration
driver.execute_script("game.keys['d'] = false;")

# Move down
driver.execute_script("game.keys['s'] = true;")
time.sleep(0.5)
driver.execute_script("game.keys['s'] = false;")
        """)
        
        print("\nPress Enter to close browser...")
        input()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()