from flask import Flask, jsonify, request
from thesis_work.UniversityTimetableData import UniversityTimetableData
from thesis_work.CSP_Algorithm import CSP_algorithm
from thesis_work.Genetic_Algorithm import genetic_algorithm
from thesis_work.LabelPlot import plot_lecturer, plot_room, plot_sg

app = Flask(__name__)
timetable_data = UniversityTimetableData('university_timetable.db')
solution = None

@app.route('/')
def index():
    return 'Welcome to the Flask server!'

@app.route('/CSP_algorithm', methods=['POST'])
def set_solution_CSP():
    global solution
    solution = CSP_algorithm(timetable_data).items() 
    return jsonify({'message': 'Soluția CSP primită'}), 200

@app.route('/genetic_algorithm', methods=['POST'])
def set_solution_GA():
    global solution
    solution = genetic_algorithm(timetable_data)
    return jsonify({'message': 'Soluția GA primită'}), 200

@app.route('/professors')
def get_professors():
    try:
        professors = [professor.professor_name for professor in timetable_data.professors]
        return jsonify({'professors': professors})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/study_programs')
def get_study_programs():
    try:
        study_programs = [study_program.program_id for study_program in timetable_data.study_programs]
        return jsonify({'study_programs': study_programs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rooms')
def get_rooms():
    try:
        rooms = [room.room_name for room in timetable_data.rooms]
        return jsonify({'rooms': rooms})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate_plot_room')
def generate_plot_room():
    try:
        choice_name = request.args.get('choice_id')
        choice_id = timetable_data.get_room_id(choice_name)
        plot_data = plot_room(timetable_data, solution, choice_id)
        return plot_data
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate_plot_professor')
def generate_plot_professor():
    try:
        choice_name = request.args.get('choice_id')
        choice_id = timetable_data.get_professor_id_by_using_name(choice_name)
        plot_data = plot_lecturer(timetable_data, solution, choice_id)
        return plot_data
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate_plot_study_program')
def generate_plot_study_program():
    try:
        choice_id = request.args.get('choice_id')
        plot_data = plot_sg(timetable_data, solution, choice_id)
        return plot_data
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)