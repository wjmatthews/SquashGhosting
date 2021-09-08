"""
Squash Ghosting

Versioning:
Luc J. - 07 Jan 2021
    Concept
    Base Ghosting class to output random location at random time interval via text

Will M. - 27 Jan 2021
    -Added wav files and loading of wav files in Ghosting.__innit__()
    -Added play_court_location() functionality
    -Added min_ti and max_ti time interval variables to top of Ghosting class
    for easier updating/tinkering
    -Updated sleep time in start_workout to use random.uniform() to allow for
    fractions of a second.
    -Implemented random_next_location to randomly choose a court location based on a
    mapped probability.
    -Moved sleep time interval to after the location announcement.  This means based on the
    location that is chosen, we can modify the length of the time interval. i.e. a drop shot
    is played, there is less time allowed.  A long drive is played, more time can be allowed.
    -Added variables/logic to track next_location, last_location, next_ti, last_ti (time interval)
    -Altered logice sequence in start_workout to accomodate changing weights of court location
    probabilities
    -Added re_weight_time_intervals functionality
    -Added re_weight_locations functionality
    -Added normalize_probs functionality
    -Added base_probs to class Ghosting and moved construction of the location:probs dictionary
    to the __init__ method of Ghosting
"""

import os
import random
import time
import simpleaudio as sa

class Ghosting:

    """
    minimum and maximum time interval variables (in seconds).  I lumped mid court shots in with drop shots for reaction time.
    feel free to play around with these!
    """
    drop_min = 1.25
    drop_max = 2.0
    drive_min = 2.0
    drive_max = 3.0

    """
    repeat_count: counts the number of times the last shot has been repated.
    repeat_max: defines the maximum number of times a shot can be repeated before the probability
    of that shot is set to 0 for the next iteration.
    repeat_inflection: when repeat_inflection == repeat_count we stop increasing the probability
    of a repeated shot, and start decreasing the probability of a repeated shot.
    
    """
    repeat_count = 0
    repeat_inflection = 2
    repeat_max = 4

    court_location_names = [
        "front_left",
        "front_right",
        "middle_left",
        "middle_right",
        "back_left",
        "back_right"
    ]

    base_probs = [
         0.15,
         0.15,
         0.05,
         0.05,
         0.30,
         0.30
    ]

    def __init__(self, duration):
        self.duration = duration

        """
        Initialize min and max time intervals
        """
        min_ti = self.drive_min
        max_ti = self.drive_max

        """
        Build court_locations dict from court_location_names and base_probs
        """
        self.court_locations = {}
        for i,loc in enumerate(self.court_location_names):
            self.court_locations.update({loc:self.base_probs[i]})

        """
        Load the wav file locations into memory via a sounds dictionary.
        """
        self.sounds = {} #dict mapping court_loactions to wav file paths
        cwd = os.getcwd()
        sounds_folder = 'Sounds'
        sounds_path = os.path.join(cwd + os.sep,sounds_folder)
        wav = '.wav'
        for location in self.court_locations :
            filename = os.path.join(sounds_path + os.sep, location) + wav
            self.sounds.update({location:filename})
        
        
    def play_court_location(self, court_location):
        """
        Takes one of six court locations as defined and plays the corresponding
        wav file
        """
        filename = self.sounds[court_location]
        wav_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wav_obj.play()

    def random_next_location(self):
        """
        Uses the dict mapping court locations to the probability of them
        occuring and returns a random court location based on the distribution.
        """
        rand_num = random.random()
        #sum up probabilities for if/elif sequence.  Implementation feels sloppy
        #and there is probably a better way to do this!
        fl = self.court_locations['front_left']
        fr = fl + self.court_locations['front_right']
        ml = fr + self.court_locations['middle_left']
        mr = ml + self.court_locations['middle_right']
        bl = mr + self.court_locations['back_left']
        br = 1
        key_lst = list(self.court_locations.keys())
        if rand_num <= fl:
            return key_lst[0]
        elif rand_num <= fr:
            return key_lst[1]
        elif rand_num <= ml:
            return key_lst[2]
        elif rand_num <= mr:
            return key_lst[3]
        elif rand_num <= bl:
            return key_lst[4]
        else:
            return key_lst[5]

    def re_weight_time_intervals(self, next_location):
        """
        Takes the next place the player has to go and modifies the range of time they have to
        complete it before being given there next location.  Less time from drop/mid court shots,
        more time to return long drives.
        """
        #play around with these until it feels right!
        if next_location != 'back_right' and next_location != 'back_left':
            self.min_ti = self.drop_min
            self.max_ti = self.drop_max
        else:
            self.min_ti = self.drive_min
            self.max_ti = self.drive_max

    def normalize_probs(self, fixed_location):
        """
        takes a location whose probability is already set to its final value.  Adjusts all other
        probabilities in court_locations so the total sum is 1.
        """
        total = sum(list(self.court_locations.values())) - self.court_locations[fixed_location]
        factor = 1 - self.court_locations[fixed_location]
        keys = list(self.court_locations.keys())
        for key in keys:
            if key != fixed_location:
                prob = self.court_locations[key]
                normalized_prob = (prob / total) * factor
                self.court_locations[key] = normalized_prob

    def re_weight_locations(self, next_location, last_location):
        """
        Re-weights the probability of the next location based on the previous and current location.
        If next shot is middle, no one plays back to the middle - reduce probs to 0 for middle
        If next shot is same as the last shot, either increase or decrease the probability of that shot
        occuring again, depending on the repeat_inflection point.
        If repeat_max has been reached, make prob of that shot/location 0.
        """

        #multipliers for increasing/decreasing the probability of an event.
        bump_up = 0.5
        cut_down = 0.5
        #do not let two middle shots be played in a row
        if next_location == 'middle_right' or next_location == 'middle_left':
            self.court_locations['middle_right'] = 0
            self.court_locations['middle_left'] = 0
            self.repeat_count = 0
            
        elif next_location == last_location:
            if self.repeat_count >= self.repeat_max:
                self.court_locations[next_location] = 0
                self.repeat_count = 0

            elif self.repeat_count < self.repeat_inflection:
                prob = self.court_locations[next_location] #get prob of next location
                inv_prob = 1 - prob #get the max amount we can increase this probability by
                prob = prob + (inv_prob * bump_up) #increase prob by the max, scaled by bump_up factor
                self.court_locations[next_location] = prob
                self.repeat_count += 1

            else: #we are greater than the inflection point.  Getting board of making same shot over
                #and over, so start reducing the probability of this shot.
                prob = self.court_locations[next_location] #get prob of next location
                prob = prob * cut_down
                self.court_locations[next_location] = prob
                self.repeat_count += 1
                
        else: #case where it is not a middle shot and not a repeat shot - assume scrambly play and
            #reset all probs to base_probs
            keys = self.court_locations.keys()
            for i, key in enumerate(keys):
                self.court_locations[key] = self.base_probs[i]
                self.repeat_count = 0
        #regardless of how next_location was altered, normalize all other probs based on next_location being fixed
        self.normalize_probs(next_location)
            
        
    def start_workout(self):
        time_end = time.time() + 60 * self.duration
        last_location = 'back_left' #need something to start.  Figured this simulates receiving a serve best.
        next_location = 'back_left'
        #last_ti = 1000 #not sure if we will need this
        print("START")
        while time.time() < time_end:
            #output next locaiton to user
            self.play_court_location(next_location)
            print(next_location) #to remove later.  Left in for debugging purposes right now
            
            #determine time interval and pause for that interval
            self.re_weight_time_intervals(next_location)
            next_ti = random.uniform(self.min_ti,self.max_ti)
            time.sleep(next_ti)

            #update variable for next loop
            last_location = next_location
            next_location = self.random_next_location()
            self.re_weight_locations(next_location, last_location)
            #last_ti = next_ti #not sure we will need
        print("END")


my_session = Ghosting(0.5)
my_session.start_workout()
