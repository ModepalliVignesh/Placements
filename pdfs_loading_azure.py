import os
import json
import requests
from xml.etree import ElementTree
from azure.storage.blob import BlobServiceClient, BlobClient
from flask import Flask, render_template, jsonify, send_file, make_response, request
import io
import logging

app = Flask(__name__)

# Azure Blob Storage connection settings
connect_str = "DefaultEndpointsProtocol=https;AccountName=placements1;AccountKey=IcnlEGgR4yyEXBaQ49jRYxadeYJlYswJzhSlq8ReqCHjsH464j1e2aPldLGaog038gAePI0J33bZ+ASt8zSdLg==;EndpointSuffix=core.windows.net"
pdf_container_name = 'interviewquestions'
video_container_name = 'interviewvideos'

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def get_sas_link(subject):
    with open("C:/vignesh/chiru/interview_videos.json", "r") as f:
        data = json.load(f)
    return data.get(subject)


@app.route('/pdfs_for_subject/<string:subject>')
def pdfs_for_subject(subject):
    # This is a placeholder logic and should be replaced with actual logic to fetch PDFs for the specified subject
    # Currently, it just returns a dummy PDF list for the given subject
    return jsonify([f"{subject}_pdf1.pdf", f"{subject}_pdf2.pdf"])
@app.route('/available_keys')
def available_keys():
    with open("C:\\vignesh\\chiru\\interview_videos.json", "r") as file:
        data = json.load(file)
    return jsonify(list(data.keys()))

@app.route('/get_video_url/<subject>')
def get_video_url(subject):
    with open("C:\\vignesh\\chiru\\interview_videos.json", "r") as file:
        data = json.load(file)
    return jsonify(data.get(subject, ""))
@app.route('/')
def index():
    return render_template('page2.html')

@app.route('/pdf/<string:filename>')
def serve_pdf(filename):
    try:
        blob_client = blob_service_client.get_blob_client(container=pdf_container_name, blob=filename)
        download_stream = blob_client.download_blob()
        pdf_bytes = download_stream.readall()
        response = make_response(pdf_bytes)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Length', len(pdf_bytes))
        response.headers.set('Content-Disposition', 'inline; filename=%s' % filename)
        return response
    except Exception as e:
        logging.exception("Failed to load PDF: %s", e)
        return make_response(f"Failed to load PDF: {e}", 500)

@app.route('/video/<string:filename>')
def serve_video(filename):
    try:
        blob_client = blob_service_client.get_blob_client(container=video_container_name, blob=filename)
        download_stream = blob_client.download_blob()
        video_bytes = download_stream.readall()
        response = make_response(video_bytes)
        response.headers.set('Content-Type', 'video/mp4')
        response.headers.set('Content-Length', len(video_bytes))
        response.headers.set('Content-Disposition', 'inline; filename=%s' % filename)
        return response
    except Exception as e:
        logging.exception("Failed to load video: %s", e)
        return make_response(f"Failed to load video: {e}", 500)

@app.route('/videos')
def list_videos():
    try:
        sas_url = get_sas_link('c')
        response = requests.get(f"{sas_url}&restype=container&comp=list")
        #logging.info(f"Raw XML response: {response.text}")
        
        root = ElementTree.fromstring(response.text)
        videos = [blob.find('Name').text for blob in root.findall('Blobs/Blob')]

        #logging.info(f"Retrieved videos: {videos}")
        return jsonify(videos)
    except Exception as e:
        logging.exception("Failed to list videos: %s", e)
        return make_response(f"Failed to list videos: {e}", 500)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, port=3000)
@app.route('/available_keys', methods=['GET'])
def available_keys():
    with open("C:\\vignesh\\chiru\\interview_videos.json", "r") as file:
        data = json.load(file)
    return jsonify(list(data.keys()))


@app.route('/pdfs_for_subject/<string:subject>', methods=['GET'])
def pdfs_for_subject(subject):
    with open("C:\\vignesh\\chiru\\interview_videos.json", "r") as file:
        data = json.load(file)
    pdfs = data.get(subject, {}).get("pdfs", [])
    return jsonify(pdfs)