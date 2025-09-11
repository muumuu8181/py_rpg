"""
Debug script for RPG game movement automation with Selenium
Tests multiple approaches to fix keyboard input issues
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException

def log_info(message):
    """Print timestamped info message"""
    print(f"[{time.strftime('%H:%M:%S')}] INFO: {message}")

def log_error(message):
    """Print timestamped error message"""
    print(f"[{time.strftime('%H:%M:%S')}] ERROR: {message}")

def get_player_position(driver):
    """Get current player position from game state"""
    try:
        # Method 1: From DOM element
        position_element = driver.find_element(By.ID, "position")
        position_text = position_element.text
        log_info(f"Position from DOM: {position_text}")
        
        # Method 2: From JavaScript game object
        js_position = driver.execute_script("""
            if (typeof game !== 'undefined' && game.player) {
                return {
                    x: game.player.x,
                    y: game.player.y,
                    facing: game.player.facing
                };
            }
            return null;
        """)
        
        if js_position:
            log_info(f"Position from JS: X:{js_position['x']}, Y:{js_position['y']}, Facing:{js_position['facing']}")
        
        return js_position
    except Exception as e:
        log_error(f"Failed to get player position: {e}")
        return None

def check_event_listeners(driver):
    """Check if event listeners are attached properly"""
    try:
        listeners = driver.execute_script("""
            // Check if we can access the game object
            const hasGame = typeof game !== 'undefined';
            
            // Try to check event listeners (limited capability)
            const hasKeyListeners = document.onkeydown !== null || window.onkeydown !== null;
            
            // Check focus
            const activeElement = document.activeElement;
            const activeTag = activeElement ? activeElement.tagName : 'none';
            
            return {
                hasGame: hasGame,
                hasKeyListeners: hasKeyListeners,
                activeElement: activeTag,
                documentHasFocus: document.hasFocus()
            };
        """)
        
        log_info(f"Event listener check: {json.dumps(listeners, indent=2)}")
        return listeners
    except Exception as e:
        log_error(f"Failed to check event listeners: {e}")
        return None

def test_movement_method_1_basic_keys(driver, canvas):
    """Method 1: Basic key sending to canvas element"""
    log_info("Testing Method 1: Basic key sending to canvas")
    
    # Focus canvas
    canvas.click()
    time.sleep(0.5)
    
    initial_pos = get_player_position(driver)
    
    # Try arrow keys
    log_info("Sending arrow keys...")
    canvas.send_keys(Keys.ARROW_RIGHT)
    time.sleep(0.5)
    canvas.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)
    
    final_pos = get_player_position(driver)
    
    if initial_pos and final_pos:
        moved = (initial_pos['x'] != final_pos['x'] or initial_pos['y'] != final_pos['y'])
        log_info(f"Movement detected: {moved}")
        return moved
    return False

def test_movement_method_2_action_chains(driver, canvas):
    """Method 2: Using ActionChains"""
    log_info("Testing Method 2: ActionChains")
    
    actions = ActionChains(driver)
    
    # Click canvas to focus
    actions.click(canvas).perform()
    time.sleep(0.5)
    
    initial_pos = get_player_position(driver)
    
    # Send keys with action chains
    log_info("Sending keys with ActionChains...")
    actions.send_keys('d').perform()  # Right
    time.sleep(0.5)
    actions.send_keys('s').perform()  # Down
    time.sleep(0.5)
    
    # Also try with key_down/key_up
    actions.key_down('w').pause(0.1).key_up('w').perform()  # Up
    time.sleep(0.5)
    
    final_pos = get_player_position(driver)
    
    if initial_pos and final_pos:
        moved = (initial_pos['x'] != final_pos['x'] or initial_pos['y'] != final_pos['y'])
        log_info(f"Movement detected: {moved}")
        return moved
    return False

def test_movement_method_3_body_keys(driver):
    """Method 3: Send keys to body element"""
    log_info("Testing Method 3: Sending keys to body")
    
    body = driver.find_element(By.TAG_NAME, "body")
    
    initial_pos = get_player_position(driver)
    
    # Send keys to body
    log_info("Sending keys to body element...")
    body.send_keys('d')  # Right
    time.sleep(0.5)
    body.send_keys('s')  # Down
    time.sleep(0.5)
    body.send_keys(Keys.ARROW_LEFT)
    time.sleep(0.5)
    
    final_pos = get_player_position(driver)
    
    if initial_pos and final_pos:
        moved = (initial_pos['x'] != final_pos['x'] or initial_pos['y'] != final_pos['y'])
        log_info(f"Movement detected: {moved}")
        return moved
    return False

def test_movement_method_4_js_dispatch(driver):
    """Method 4: Dispatch keyboard events via JavaScript"""
    log_info("Testing Method 4: JavaScript event dispatching")
    
    initial_pos = get_player_position(driver)
    
    # JavaScript to dispatch keyboard events
    js_code = """
    function dispatchKeyEvent(key, keyCode, type='keydown') {
        const event = new KeyboardEvent(type, {
            key: key,
            keyCode: keyCode,
            code: key,
            bubbles: true,
            cancelable: true
        });
        document.dispatchEvent(event);
    }
    
    // Move right
    dispatchKeyEvent('d', 68, 'keydown');
    setTimeout(() => dispatchKeyEvent('d', 68, 'keyup'), 100);
    
    // Move down after a delay
    setTimeout(() => {
        dispatchKeyEvent('s', 83, 'keydown');
        setTimeout(() => dispatchKeyEvent('s', 83, 'keyup'), 100);
    }, 200);
    
    return true;
    """
    
    try:
        driver.execute_script(js_code)
        time.sleep(1)
        
        final_pos = get_player_position(driver)
        
        if initial_pos and final_pos:
            moved = (initial_pos['x'] != final_pos['x'] or initial_pos['y'] != final_pos['y'])
            log_info(f"Movement detected: {moved}")
            return moved
    except Exception as e:
        log_error(f"JavaScript execution failed: {e}")
    
    return False

def test_movement_method_5_direct_manipulation(driver):
    """Method 5: Directly manipulate game state via JavaScript"""
    log_info("Testing Method 5: Direct game state manipulation")
    
    initial_pos = get_player_position(driver)
    
    # Directly set key states in game object
    js_code = """
    if (typeof game !== 'undefined' && game.keys !== undefined) {
        // Simulate right key press
        game.keys['d'] = true;
        game.keys['D'] = true;
        
        // Let it process for a few frames
        setTimeout(() => {
            game.keys['d'] = false;
            game.keys['D'] = false;
            
            // Then simulate down key
            game.keys['s'] = true;
            game.keys['S'] = true;
            
            setTimeout(() => {
                game.keys['s'] = false;
                game.keys['S'] = false;
            }, 200);
        }, 200);
        
        return true;
    }
    return false;
    """
    
    try:
        result = driver.execute_script(js_code)
        if result:
            log_info("Successfully set game.keys states")
            time.sleep(1)
            
            final_pos = get_player_position(driver)
            
            if initial_pos and final_pos:
                moved = (initial_pos['x'] != final_pos['x'] or initial_pos['y'] != final_pos['y'])
                log_info(f"Movement detected: {moved}")
                return moved
        else:
            log_error("Could not access game.keys object")
    except Exception as e:
        log_error(f"JavaScript execution failed: {e}")
    
    return False

def test_movement_method_6_focus_variations(driver, canvas):
    """Method 6: Try various focus techniques"""
    log_info("Testing Method 6: Various focus techniques")
    
    initial_pos = get_player_position(driver)
    
    # Try different focus methods
    try:
        # Method 1: JavaScript focus
        driver.execute_script("arguments[0].focus();", canvas)
        time.sleep(0.5)
        
        # Method 2: Click and tab
        canvas.click()
        time.sleep(0.2)
        
        # Method 3: Focus body then canvas
        driver.execute_script("document.body.focus();")
        time.sleep(0.2)
        driver.execute_script("document.getElementById('gameCanvas').focus();")
        time.sleep(0.5)
        
        # Now try sending keys
        canvas.send_keys('dddsss')  # Right right right, down down down
        time.sleep(1)
        
        final_pos = get_player_position(driver)
        
        if initial_pos and final_pos:
            moved = (initial_pos['x'] != final_pos['x'] or initial_pos['y'] != final_pos['y'])
            log_info(f"Movement detected: {moved}")
            return moved
            
    except Exception as e:
        log_error(f"Focus method failed: {e}")
    
    return False

def main():
    """Main test function"""
    log_info("Starting RPG Game Movement Debug Script")
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Load the game
        game_url = "file:///C:/Users/user/Desktop/work/90_cc/20250910/minimal-rpg-game/custom_bg_game.html"
        log_info(f"Loading game from: {game_url}")
        driver.get(game_url)
        
        # Wait for canvas to load
        canvas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gameCanvas"))
        )
        log_info("Canvas element found")
        
        # Give game time to initialize
        time.sleep(2)
        
        # Check initial state
        log_info("=== Initial State Check ===")
        check_event_listeners(driver)
        initial_position = get_player_position(driver)
        
        # Test all movement methods
        methods = [
            ("Basic Keys", lambda: test_movement_method_1_basic_keys(driver, canvas)),
            ("ActionChains", lambda: test_movement_method_2_action_chains(driver, canvas)),
            ("Body Keys", lambda: test_movement_method_3_body_keys(driver)),
            ("JS Event Dispatch", lambda: test_movement_method_4_js_dispatch(driver)),
            ("Direct State Manipulation", lambda: test_movement_method_5_direct_manipulation(driver)),
            ("Focus Variations", lambda: test_movement_method_6_focus_variations(driver, canvas))
        ]
        
        results = []
        
        for method_name, method_func in methods:
            log_info(f"\n=== Testing {method_name} ===")
            
            # Reset position if we can
            try:
                driver.execute_script("""
                    if (typeof game !== 'undefined' && game.player) {
                        game.player.x = 400;
                        game.player.y = 300;
                    }
                """)
            except:
                pass
            
            time.sleep(0.5)
            success = method_func()
            results.append((method_name, success))
            
            # Give time between tests
            time.sleep(1)
        
        # Summary
        log_info("\n=== Test Results Summary ===")
        for method, success in results:
            status = "✅ WORKED" if success else "❌ FAILED"
            log_info(f"{method}: {status}")
        
        # Additional debugging info
        log_info("\n=== Additional Debug Info ===")
        
        # Check if game loop is running
        game_state = driver.execute_script("""
            return {
                gameExists: typeof game !== 'undefined',
                frameCount: typeof game !== 'undefined' ? game.frameCount : -1,
                keysObject: typeof game !== 'undefined' ? Object.keys(game.keys).filter(k => game.keys[k]) : []
            };
        """)
        log_info(f"Game state: {json.dumps(game_state, indent=2)}")
        
        # Keep browser open for manual inspection
        log_info("\nPress Enter to close browser...")
        input()
        
    except Exception as e:
        log_error(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    main()