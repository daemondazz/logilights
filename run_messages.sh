#!/bin/bash

cleanup() {
	echo "running cleanup"
	killall timeout
	exit
}

run_cmd_timeout() {
	timeout --preserve-status -k 5 $* &
	PID=$!
	wait $PID
}

seconds_till() {
	local current_ts=$( date +%s )
	local end_ts=$1
	echo $(( $end_ts - $current_ts))
}

# Make sure we cleanup children
trap cleanup SIGINT
trap cleanup SIGTERM

# Keep running forever
while /bin/true; do

	# Some helper variables
	eval $( date +YEAR=%Y\;MONTH=%m\;DAY=%d\;HOUR=%H\;MIN=%M )

	# If it's Christmas day, just run our Merry Christmas panel until midnight
	if [[ "${MONTH}-${DAY}" == "12-25" ]]; then
		run_cmd_timeout $( seconds_till $( date -d "tomorrow 00:00:00" +%s )) \
		         software/python/two_line_text.py merry_christmas_today.json

	# If we are in December and it's before Christmas, show the seasons greetings
	# and sleeps remaining panels
	elif [[ ${MONTH} -eq 12 && ${DAY} -lt 25 ]]; then

		# Between ww:55 and xx:10 show sleeps left
		# Between xx:10 and xx:25 show seasons greetings
		# Between xx:25 and xx:40 show sleeps left
		# Between xx:40 and xx:55 show seasons greetings
		if [[ ${MIN} -lt 10 ]]; then
			SCRIPT="days"
		elif [[ ${MIN} -lt 25 ]]; then
			SCRIPT="greetings"
		elif [[ ${MIN} -lt 40 ]]; then
			SCRIPT="days"
		elif [[ ${MIN} -lt 55 ]]; then
			SCRIPT="greetings"
		else
			SCRIPT="days"
		fi

		# Work out the next time we have to switch panels
		# If we've already passed the 10 minutes offset from the last quarter hour
		# chime, skip to the next one
		NEXT_ROLLOVER=$(( $( date +%s) - ($(date +%s) % (15 * 60)) + 600 ))
		if [[ $( seconds_till ${NEXT_ROLLOVER} ) -le 0 ]]; then
			NEXT_ROLLOVER=$(( ${NEXT_ROLLOVER} + 900))
		fi

		# Run the chosen script
		if [[ "${SCRIPT}" == "days" ]]; then
			run_cmd_timeout $( seconds_till ${NEXT_ROLLOVER}) \
			         software/python/days_to_go.py ${YEAR}-12-25
		else
			run_cmd_timeout $( seconds_till ${NEXT_ROLLOVER}) \
			         software/python/two_line_text.py merry_christmas_languages.json
		fi

	# If we are in December and it's after Christmas, just show the seasons
	# greetings panels
	elif [[ ${MONTH} -eq 12 && ${DAY} -gt 25 ]]; then
		run_cmd_timeout $( seconds_till $( date -d "tomorrow 00:00:00" +%s )) \
		         software/python/two_line_text.py merry_christmas_languages.json

	# Otherwise, if it's not December, show current time and temperature panel
	else
		run_cmd_timeout $( seconds_till $( date -d "tomorrow 00:00:00" +%s )) \
		         software/python/time_and_temperature.py

	fi
	sleep 1
done