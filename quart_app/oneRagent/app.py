from quart import Quart, render_template, jsonify
from onlyRagent import eng_papers, eth_papers, pol_papers

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/api/papers')
async def get_papers():
    engineer_paper = await eng_papers()
    ethicist_paper = await eth_papers()
    policyMaker_paper = await pol_papers()
    papers = {
        "engineer_paper": engineer_paper,
        "ethicist_paper": ethicist_paper,
        "policyMaker_paper": policyMaker_paper
    }
    print("Fetched papers:", papers)  
    return jsonify(papers)

if __name__ == "__main__":
    app.run(debug=True)
