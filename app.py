import csv
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Function to load mentors from a CSV file
def load_mentors_from_csv():
    mentors = []
    with open('mentors.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mentor = {
                'name': row['name'],
                'subjects': row['subjects'].split('|'),
                'rating': float(row['rating']),
                'prep_level': int(row['prep_level']),
                'learning_style': row['learning_style'],
                'target_colleges': row['target_colleges'].split(';')
            }
            mentors.append(mentor)
    return mentors

# Function to recommend mentors based on aspirant's data
def recommend_mentors(aspirant_data):
    mentors = load_mentors_from_csv()
    matched_mentors = []

    for mentor in mentors:
        match_score = 0

        # Match preferred subject(s)
        if aspirant_data['preferred_subject'] in mentor['subjects']:
            match_score += 1
        
        # Match learning style
        if aspirant_data['learning_style'] == mentor['learning_style']:
            match_score += 1
        
        # Match preparation level
        if aspirant_data['prep_level'] == mentor['prep_level']:
            match_score += 1
        
        # Match target college
        if aspirant_data['target_college'] in mentor['target_colleges']:
            match_score += 1
        
        if match_score > 0:
            # ✅ BONUS IMPROVEMENT: Boost score with mentor rating (scaled)
            final_score = match_score + (mentor['rating'] / 5)  # Normalize rating to 0-1 scale
            matched_mentors.append({'mentor': mentor, 'match_score': final_score})

    # Sort by score in descending order
    matched_mentors.sort(key=lambda x: x['match_score'], reverse=True)

    # Return top 3
    return matched_mentors[:3]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    aspirant_data = request.json
    matched_mentors = recommend_mentors(aspirant_data)

    recommendations = [{
        'name': mentor['mentor']['name'],
        'rating': mentor['mentor']['rating'],
        'match_score': round(mentor['match_score'], 2)  # Optional: round for readability
    } for mentor in matched_mentors]

    return jsonify({'mentors': recommendations})

@app.route('/rate_mentor', methods=['POST'])
def rate_mentor():
    data = request.json
    mentor_name = data['mentor_name']
    rating = float(data['rating'])

    mentors = load_mentors_from_csv()
    for mentor in mentors:
        if mentor['name'] == mentor_name:
            # ✅ BONUS IMPROVEMENT: Smarter rating update could use a count, but keep it simple for now
            mentor['rating'] = (mentor['rating'] + rating) / 2
            break

    with open('mentors.csv', mode='w', newline='') as file:
        fieldnames = ['name', 'subjects', 'rating', 'prep_level', 'learning_style', 'target_colleges']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for mentor in mentors:
            writer.writerow({
                'name': mentor['name'],
                'subjects': '|'.join(mentor['subjects']),
                'rating': mentor['rating'],
                'prep_level': mentor['prep_level'],
                'learning_style': mentor['learning_style'],
                'target_colleges': ';'.join(mentor['target_colleges'])
            })

    return jsonify({'message': 'Rating submitted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
