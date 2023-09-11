
from flask import Flask, request, jsonify
from some_crawling_library import QueenitCrawler
from autoencoder_model import Autoencoder
from clustering import perform_clustering
from save_model_and_cluster_info import save_to_csv_and_hash

app = Flask(__name__)

@app.route('/crawl', methods=['POST'])
def crawl():
    # Step 1: Crawling
    crawler = QueenitCrawler()
    crawler.crawl_images()

    # Step 2: Image saving is done in the crawling function

    # Step 3: Latent Vector Extraction and Model Saving
    autoencoder = Autoencoder()
    latent_vectors = autoencoder.extract_latent_vectors()

    # Step 4: Clustering and Cluster Center Distance Calculation
    df = perform_clustering(latent_vectors)

    # Step 5: Save to CSV and Hash Table
    save_to_csv_and_hash(df)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
