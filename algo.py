def calculate_delay_and_volume(self, click_x, click_y):
    scaler=60 
    sensors_delta=0.5 # distance between the left and right microphones
    sound_speed=343 #Speed of sound in mps
    meter_multiplier=1
    try:
        center_x = 300
        center_y = 300
        x_dist = click_x - center_x
        y_dist = click_y - center_y

        left_distance = (math.sqrt((x_dist + sensors_delta / 2)**2 + y_dist**2))/scaler
        right_distance = (math.sqrt((x_dist - sensors_delta / 2)**2 + y_dist**2))/scaler

        left_delay = (left_distance / sound_speed) * meter_multiplier
        right_delay = (right_distance / sound_speed) * meter_multiplier

        if left_delay<right_delay:
            left_volume=1
            right_volume=0.4
        elif left_delay>right_delay:
            right_volume=1
            left_volume=0.4
        else:
            left_volume=1
            right_volume=1

        if left_delay < right_delay:
            left_volume = 1 / (0.2 + left_distance * 0.5)
            right_volume = 1 / (0.4 + left_distance)       
        elif left_delay > right_delay:
            right_volume = 1 / (0.2 + right_distance * 0.5)
            left_volume = 1 / (0.4 + right_distance)
        else:
            left_volume = 1
            right_volume = 1

        return left_delay, right_delay, left_volume, right_volume
    except Exception as e:
        print(f"Error calculating: {e}")