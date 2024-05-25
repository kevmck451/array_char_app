import os

def base_path(relative_path):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(current_script_dir))
    return os.path.join(base_dir, relative_path)

# Main App Settings
window_title = 'Acoustic Phase Array Characterization Experiment'

window_width = 1300
window_height = 640
min_window_width = window_width
min_window_height = window_height

x_pad_main = 2
y_pad_main = 2
x_pad_1 = 10
y_pad_1 = 10
x_pad_2 = 10
y_pad_2 = 10
main_font_style = "default_font"
main_font_size = 20 #26

playing_icon_filepath = base_path('control/docs/playing icon s.png')
playing_icon_s_filepath = base_path('control/docs/playing icon ss.png')
start_icon_filepath = base_path('control/docs/start icon s.png')
stop_icon_filepath = base_path('control/docs/stop icon s.png')
pause_icon_filepath = base_path('control/docs/pause icon s.png')
load_icon_filepath = base_path('control/docs/load icon s.png')
settings_icon_filepath = base_path('control/docs/settings icon s.png')
reset_icon_filepath = base_path('control/docs/reset icon s.png')

button_fg_color = '#578CD5' # blue
button_hover_color = '#496FA3' # blue
dropdown_hover_color = '#0F5BB6'
dropdown_fg_color = '#0952AA'

# Console Settings
console_x_pad = 5
console_y_pad = 1
console_font_style = ("default_font", 12)

# Main Frame Settings

# Hardware Frame Settings
connection_status_TDT = 'TDT Hardware: Not Connected'
connection_status_TDT_C = 'TDT Hardware: Connected'
connection_status_VR = 'Controller: Not Connected'
connection_status_VR_C = 'Controller: Connected'
not_connected_color = '#BD2E2E'
connected_color = '#2B881A'

# Select Experiment Settings

# Warm Up
warmup_test_color = 'gray'
warmup_neutral_bg_color = '#DBDBDB'
warmup_playing_bg_color = '#B8B9B8'


# Start / Stop
start_fg_color="#2B881A"
start_hover_color='#389327'
stop_fg_color="#BD2E2E"
stop_hover_color='#C74343'

# Pause Frame
pause_fg_color = '#8F8F8F'
pause_hover_color = '#9E9E9E'

# Settings Button
settings_fg_color = '#4a4949'
settings_hover_color = '#5c5b5b'

# Reset Button
reset_fg_color = '#8270E7'
reset_hover_color = '#8F7FE9'









