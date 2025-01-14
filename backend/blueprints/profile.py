""" Defines routes for the profile page """

from flask import Blueprint, request, jsonify, session, current_app, Response
from ..models import *
from sqlalchemy import select

profile_blueprint = Blueprint('profile', __name__, 
                              template_folder='../../templates', 
                              static_folder='../../static')

@profile_blueprint.route('/save_schedule', methods=['POST'])
def save_schedule() -> tuple[Response, int]:
    """
    Handles a POST request to save a user's schedule availability.
    It first retrieves the schedule data from the request, checks for any existing availability blocks for the user, 
    deletes them if found, and then inserts the new availability blocks into the database. 
    If any error occurs during this process, it rolls back the transaction and returns an error response.
    If success, it commits the changes and returns a success message.

    :author: Tony Chen
    :version: 2023.11.29
    """

    # Get information from the user
    data = request.get_json()
    schedules = data['schedule']
    user_email = session.get('email') or 'no_email'
    try:
        # Check for existing availability blocks for the user
        existing_blocks = current_app.db.session.query(AvailabilityBlock).filter(AvailabilityBlock.user_email == user_email).all()


        # If existing availability blocks are found, delete them
        if existing_blocks:
            current_app.db.session.query(AvailabilityBlock).filter(AvailabilityBlock.user_email == user_email).delete() #TODO: update the outdated query

        # Insert new availability blocks
        for schedule in schedules:
            new_availability = AvailabilityBlock(
                start_day=schedule['day'],
                end_day=schedule['day'],
                start_time=schedule['startTime'],
                end_time=schedule['endTime'],
                user_email=user_email
            )
            current_app.db.session.add(new_availability)

        # Commit changes to the database
        current_app.db.session.commit()

    except Exception as e:
        print(f"Exception occurred: {e}")
        current_app.db.session.rollback()
        return jsonify({'error': str(e)}), 500

    # Return a successful response
    return jsonify({'message': 'Schedule saved successfully'}), 201  #TODO: sync the change


@profile_blueprint.route('/get_schedule', methods=['GET'])
def get_schedule() -> tuple[Response, int]:
    """
    Handles a GET request to retrieve the schedule availability of the current logged-in user.
    It queries the database for availability blocks associated with the user's email.
    The function formats these blocks into a JSON-serializable format and returns them.
    If an exception occurs during database operations, an error response is returned.

    :author: Tony Chen
    :version: 2023.11.29
    """


    # Retrieve the user's email from the session
    user_email = session.get('email')

    try:
        # Query for getting the availability blocks of the current user
        avail_blocks = current_app.db.session.query(AvailabilityBlock).filter(AvailabilityBlock.user_email == user_email).all() #TODO: update? see the models.py

        # Initialize an empty list for the formatted data
        avail_blocks_data = []

        # Loop through each availability block and format the data
        for block in avail_blocks:
            formatted_block = {
                'day': block.start_day,
                'startTime': block.start_time.strftime("%H:%M"),  # Assuming start_time is a datetime.time object
                'endTime': block.end_time.strftime("%H:%M")       # Assuming end_time is a datetime.time object
            }
            avail_blocks_data.append(formatted_block)

        # Return the availability blocks data
        return jsonify(avail_blocks_data), 200

    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500