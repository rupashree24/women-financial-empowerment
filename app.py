import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if request.method == 'POST':
        try:
            # Get form inputs
            income = float(request.form['income'])
            grocery = float(request.form.get('grocery', 0))
            medicine = float(request.form.get('medicine', 0))
            maintenance = float(request.form.get('maintenance', 0))
            shopping = float(request.form.get('shopping', 0))
            other = float(request.form.get('other', 0))

            # Calculate total expenses and savings
            total_expenses = grocery + medicine + maintenance + shopping + other
            savings = income - total_expenses

            return render_template('budget.html', 
                                   savings=savings, 
                                   total_expenses=total_expenses,
                                   grocery=grocery, 
                                   medicine=medicine, 
                                   maintenance=maintenance, 
                                   shopping=shopping, 
                                   other=other)
        except ValueError:
            return render_template('budget.html', error="Please enter valid numbers.")

    return render_template('budget.html', savings=None)


@app.route('/portfolio')
def portfolio():
    investments = {"Stocks": 15000, "Bonds": 10000, "Mutual Funds": 5000}
    total_value = sum(investments.values())
    return render_template('portfolio.html', investments=investments, total_value=total_value)

@app.route('/resource')
def resources():
    return render_template('resource.html')

@app.route('/sipcalc', methods=['GET', 'POST'])
def sipcalc():
    if request.method == 'POST':
        monthly_contribution = float(request.form['monthly_contribution'])
        rate_of_return = float(request.form['rate_of_return']) / 100
        years = int(request.form['years'])
        
        # SIP formula: A = P * [(1 + r)^n - 1] / r
        total_value = monthly_contribution * (((1 + rate_of_return / 12) ** (years * 12) - 1) / (rate_of_return / 12))
        return render_template('sipcalc.html', total_value=round(total_value, 2))
    return render_template('sipcalc.html')

@app.route('/emi', methods=['GET', 'POST'])
def emi():
    if request.method == 'POST':
        loan_amount = float(request.form['loan_amount'])
        rate_of_interest = float(request.form['rate_of_interest']) / 100
        loan_term = int(request.form['loan_term'])
        
        # EMI formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
        monthly_interest_rate = rate_of_interest / 12
        emi = loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_term) / ((1 + monthly_interest_rate) ** loan_term - 1)
        return render_template('emi.html', emi=round(emi, 2))
    return render_template('emi.html')

@app.route('/games')
def games():
    return render_template('games.html')


@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question")
    
    if not user_input:
        return jsonify({"error": "No question provided!"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        answer = response["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

community_posts = []

@app.route('/community', methods=['GET', 'POST'])
def community():
    if request.method == 'POST':
        username = request.form['username']
        post_content = request.form['post_content']

        if username and post_content:
            # Add new post
            community_posts.append({'username': username, 'post_content': post_content, 'replies': [], 'votes': 0})

    return render_template('community.html', posts=community_posts)

@app.route('/reply/<int:post_index>', methods=['POST'])
def reply(post_index):
    reply_content = request.form['reply_content']
    if reply_content and 0 <= post_index < len(community_posts):
        community_posts[post_index]['replies'].append(reply_content)
    return redirect(url_for('community'))

@app.route('/upvote/<int:post_index>')
def upvote(post_index):
    if 0 <= post_index < len(community_posts):
        community_posts[post_index]['votes'] += 1
    return redirect(url_for('community'))

@app.route('/downvote/<int:post_index>')
def downvote(post_index):
    if 0 <= post_index < len(community_posts):
        community_posts[post_index]['votes'] -= 1
    return redirect(url_for('community'))

if __name__ == "__main__":
    app.run(debug=True)
