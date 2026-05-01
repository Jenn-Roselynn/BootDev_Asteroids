import inspect # For accessing local variables of the caller
import json # For writing logs in JSON format
import math # For calculating elapsed time in seconds
from datetime import datetime # For timestamping log entries

__all__ = ["log_state", "log_event"] # Expose only the logging functions

_FPS = 60 # Assuming the game runs at 60 frames per second
_MAX_SECONDS = 16 # Maximum duration to log game state (in seconds). After this, state logging will stop to prevent excessive log size. Adjust as needed.
_SPRITE_SAMPLE_LIMIT = 10  # Maximum number of sprites to log per group

_frame_count = 0 # Global frame counter to track how many frames have been logged. 
_state_log_initialized = False # Flag to track if the state log file has been initialized. 
_event_log_initialized = False # Flag to track if the event log file has been initialized. 
_start_time = datetime.now() # Timestamp to mark the start of logging. 

def log_state():# This logs relevant information such as screen size and details about sprites in groups, while also managing log file creation and ensuring that logging stops after a certain duration to prevent excessive log sizes.
    global _frame_count, _state_log_initialized # Access the global frame count and state log initialization flag to manage logging behavior across multiple calls to this function. The frame count helps in determining when to stop logging based on the maximum duration defined by _MAX_SECONDS, while the initialization flag ensures that we create a new log file on the first call and append to it for subsequent calls, preventing overwriting logs from previous runs.

    # Stop logging after `_MAX_SECONDS` seconds
    if _frame_count > _FPS * _MAX_SECONDS:
        return

    # Take a snapshot approx. once per second
    _frame_count += 1
    if _frame_count % _FPS != 0:
        return
    now = datetime.now() # Capture the current timestamp to include in the log entry. 

    frame = inspect.currentframe() # Get the current stack frame to access the local variables of the caller. 
    if frame is None: # If we can't access the frame for some reason, we won't be able to log the game state, so we simply return without doing anything. 
        return
    frame_back = frame.f_back # Move one frame back to access the caller's local variables, which contain the game state information we want to log. 
    if frame_back is None: # If we can't access the caller's frame for some reason, we won't be able to log the game state, so we simply return without doing anything. 
        return

    local_vars = frame_back.f_locals.copy() # Copy the local variables of the caller to avoid any issues with mutability or changes to the original variables while we are processing them for logging. 
    screen_size = [] # Initialize an empty list to store the screen size if we find it in the local variables.
    game_state = {} # Initialize an empty dictionary to store the game state information that we extract from the local variables.

    for key, value in local_vars.items(): # Iterate through the local variables of the caller to find relevant game state information. 
        if "pygame" in str(type(value)) and hasattr(value, "get_size"): # Check if the variable is a Pygame surface (which typically represents the screen) by looking for "pygame" in its type and checking if it has a "get_size" method.
            screen_size = value.get_size() # If we find a Pygame surface, we will log its size as the screen size in our log entry. This gives us information about the dimensions of the game window at the time of logging, which can be useful for analyzing how the game state relates to the screen size.

        if hasattr(value, "__class__") and "Group" in value.__class__.__name__: # Check if the variable is a sprite group by looking for a class name that contains "Group". 
            sprites_data = [] # Initialize an empty list to store information about the sprites in the group. 

            for i, sprite in enumerate(value): # Iterate through the sprites in the group, using enumerate to keep track of how many sprites we have processed. 
                if i >= _SPRITE_SAMPLE_LIMIT: # If we have processed enough sprites from this group (as defined by _SPRITE_SAMPLE_LIMIT), we will stop processing further sprites to prevent excessive log sizes. 
                    break

                sprite_info = {"type": sprite.__class__.__name__} # Create a dictionary to store information about the current sprite, starting with its type (class name). 

                if hasattr(sprite, "position"): # If the sprite has a "position" attribute, we will log its position as a list of [x, y] coordinates, rounded to 2 decimal places for readability.  
                    sprite_info["pos"] = [ # If the sprite has a "position" attribute, we will log its position as a list of [x, y] coordinates, rounded to 2 decimal places for readability. 
                        round(sprite.position.x, 2), # If the sprite has a "position" attribute, we will log its position as a list of [x, y] coordinates, rounded to 2 decimal places for readability. 
                        round(sprite.position.y, 2),  
                    ]

                if hasattr(sprite, "velocity"): # If the sprite has a "velocity" attribute, we will log its velocity as a list of [x, y] components, rounded to 2 decimal places for readability. 
                    sprite_info["vel"] = [ # If the sprite has a "velocity" attribute, we will log its velocity as a list of [x, y] components, rounded to 2 decimal places for readability. 
                        round(sprite.velocity.x, 2), # If the sprite has a "velocity" attribute, we will log its velocity as a list of [x, y] components, rounded to 2 decimal places for readability. 
                        round(sprite.velocity.y, 2), 
                    ]

                if hasattr(sprite, "radius"): # If the sprite has a "radius" attribute, we will log its radius. 
                    sprite_info["rad"] = sprite.radius # If the sprite has a "radius" attribute, we will log its radius. 

                if hasattr(sprite, "rotation"): # If the sprite has a "rotation" attribute, we will log its rotation, rounded to 2 decimal places for readability. 
                    sprite_info["rot"] = round(sprite.rotation, 2)  # If the sprite has a "rotation" attribute, we will log its rotation, rounded to 2 decimal places for readability. 
                sprites_data.append(sprite_info)  # Add the collected information about this sprite to our list of sprite data for the group. 

            game_state[key] = {"count": len(value), "sprites": sprites_data}  # After processing the sprites in this group, we will store the collected information in our game_state dictionary under the key that corresponds to the variable name of the group. This allows us to organize our log entry in a structured way, making it easier to analyze and understand the state of the game at the time of logging. We will include both the count of how many sprites are in the group and a list of details about the individual sprites we logged, providing insights into the current conditions of the game at that moment.

        # CHANGED: Updated condition to explicitly check for Player class
        # This ensures the player object is logged even if game_state has other entries
        # The condition now looks for any object with a "position" attribute that is a Player
        if len(game_state) == 0 and hasattr(value, "position"): # and "Player" in str(type(value)):
            sprite_info = {"type": value.__class__.__name__} # CHANGED: Log the actual class name of the player object instead of hardcoding "Player"
            
            # Log the player's position as [x, y] rounded to 2 decimal places
            sprite_info["pos"] = [
                round(value.position.x, 2),
                round(value.position.y, 2),
            ]

            # If player has velocity, log it as well
            if hasattr(value, "velocity"): # CHANGED: Added condition to check for velocity attribute, which is common in player objects. 
                sprite_info["vel"] = [
                    round(value.velocity.x, 2),
                    round(value.velocity.y, 2),
                ]

            # If player has radius (from CircleShape), log it
            if hasattr(value, "radius"): # CHANGED: Added condition to check for radius attribute, which is common in CircleShape. 
                sprite_info["rad"] = value.radius

            # If player has rotation attribute, log it
            if hasattr(value, "rotation"): # CHANGED: Added condition to check for rotation attribute, which is common in player objects. 
                sprite_info["rot"] = round(value.rotation, 2)

            # Store player info in game_state using the variable name as key
            game_state[key] = sprite_info # CHANGED: Store the player info directly in game_state with the variable name as key, instead of under a "sprites" list. 

    entry = {
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3], # Format as HH:MM:SS.mmm
        "elapsed_s": math.floor((now - _start_time).total_seconds()), # Elapsed time in seconds, rounded down
        "frame": _frame_count, # Current frame count
        "screen_size": screen_size, # Screen size if found, else empty list
        **game_state, # Unpack the game state data collected from local variables
    }

    # New log file on each run
    mode = "w" if not _state_log_initialized else "a" # Use "w" mode to create a new log file on the first log entry, and "a" mode to append to the existing log file for subsequent entries. 
    with open("game_state.jsonl", mode) as f: # Open the log file in the appropriate mode (write or append) to ensure that we create a new log file for each run of the game while still allowing us to append new log entries to the existing file during the same run. 
        f.write(json.dumps(entry) + "\n") # Write the log entry as a JSON object followed by a newline character to create a JSON Lines format log file. This allows us to easily parse the log file later, as each line represents a separate JSON object containing details about the game state at a specific moment in time.
    _state_log_initialized = True # Set the state log initialization flag to True after the first log entry is written, ensuring that subsequent calls to this function will append to the existing log file instead of creating a new one. This allows us to maintain a continuous log of game states for each execution of the game without overwriting previous logs.


def log_event(event_type, **details): # This function logs specific game events, such as player actions or significant occurrences in the game. It captures the event type and any additional details provided as keyword arguments, along with a timestamp and elapsed time since logging started. Similar to log_state, it manages log file creation and appending to ensure that logs are organized and preserved across multiple runs of the game.
    global _event_log_initialized # Access the global event log initialization flag to manage logging behavior across multiple calls to this function. The initialization flag ensures that we create a new log file for events on the first call and append to it for subsequent calls, preventing overwriting logs from previous runs.


    now = datetime.now() # Capture the current timestamp to include in the log entry. 

    event = { # Construct the event log entry as a dictionary, including the timestamp, elapsed time in seconds, current frame count, event type, and any additional details provided as keyword arguments. This structured format allows us to capture important information about the event in a way that is easy to analyze later, providing insights into what happened in the game and when it occurred.
        "timestamp": now.strftime("%H:%M:%S.%f")[:-3], # Format the timestamp as HH:MM:SS.mmm for consistency with state logs and to provide precise timing information for when the event occurred.
        "elapsed_s": math.floor((now - _start_time).total_seconds()), # Calculate the elapsed time in seconds since logging started, rounded down to the nearest whole second. This allows us to understand how much time has passed in the game when the event occurred, which can be useful for analyzing the timing of events in relation to changes in the game state.
        "frame": _frame_count, # Include the current frame count in the event log entry to provide a reference for when the event occurred in terms of game frames. This can be useful for correlating events with specific moments in the game and understanding how they relate to changes in the game state over time.
        "type": event_type, # Include the type of event being logged, which is provided as an argument to the function. This allows us to categorize events and analyze them based on their type, providing insights into what kinds of actions or occurrences are happening in the game.
        **details, # Unpack any additional details provided as keyword arguments into the event log entry. This allows us to include specific information about the event, such as which player performed an action, what the action was, or any other relevant data that can help us understand the context of the event and analyze it later.
    }

    mode = "w" if not _event_log_initialized else "a" # Use "w" mode to create a new log file for events on the first log entry, and "a" mode to append to the existing log file for subsequent entries. This ensures that we don't overwrite logs from previous runs and allows us to maintain a continuous log of events for each execution of the game.
    with open("game_events.jsonl", mode) as f:  # Open the event log file in the appropriate mode (write or append) to ensure that we create a new log file for events on the first run of the game while still allowing us to append new event log entries to the existing file during the same run. This helps us maintain organized logs without losing data from previous runs.
        f.write(json.dumps(event) + "\n") # Write the event log entry as a JSON object followed by a newline character to create a JSON Lines format log file. This allows us to easily parse the log file later, as each line represents a separate JSON object containing details about a specific event that occurred in the game.

    _event_log_initialized = True # Set the event log initialization flag to True after the first event log entry is written, ensuring that subsequent calls to this function will append to the existing event log file instead of creating a new one. This allows us to maintain a continuous log of events for each execution of the game without overwriting previous logs.
