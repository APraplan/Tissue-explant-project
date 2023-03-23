# Control table address
# config EEPROM
ADDR_OPERATING_MODE         = 11
ADDR_CURRENT_LIMIT          = 38
ADDR_MAX_POSITION_LIMIT     = 48
ADDR_MIN_POSITION_LIMIT     = 52

# Config RAM
ADDR_TORQUE_ENABLE          = 64         
ADDR_LED                    = 65

# Reading
ADDR_PRESENT_POSITION       = 132
ADDR_PRESENT_VELOCITY       = 128
ADDR_PRESENT_CURRENT        = 126
ADDR_PRESENT_PWM            = 124

# Writing
ADDR_GOAL_POSITION          = 116
ADDR_GOAL_VELOCITY          = 104
ADDR_GOAL_CURRENT           = 102
ADDR_GOAL_PWM               = 100
ADDR_PROFILE_VELOCITY       = 112
ADDR_PROFILE_ACCELERATION   = 108

# Status
ADDR_MOVING                 = 122
ADDR_MOVING_STATUS          = 123


operating_modes_xm = {
                    "current": 0,
                    "velocity": 1,
                    "position": 3,
                    "extended position": 4,
                    "current-based position": 5,
                    "pwm": 16
                }

operating_modes_xl = {
                    "velocity": 1,
                    "position": 3,
                    "extended position": 4,
                    "pwm": 16
                }


# 2s complement conversion
max_register_value = {
                        "current": 65536,
                        "pwm": 65536,
                        "position": 4294967296,
                        "velocity": 4294967296,
                        "1 byte": 256,
                        "2 bytes": 65536,
                        "4 bytes": 4294967296
                    }