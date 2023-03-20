from flask import Blueprint, render_template,request,jsonify, redirect, url_for

views =Blueprint(__name__, "views")
import requests


@views.route("/")
def home():
    return render_template("index.html", name="there")

@views.route("/profile")
def profile():
    args = request.args
    name = args.get("name")
    return render_template("profile.html", name=name)

@views.route("/json")
def get_json():
    return jsonify({"name":"tim", "cool":10})

#access json from data
@views.route("/data")
def get_data():
    data=request.json
    return jsonify(data)

