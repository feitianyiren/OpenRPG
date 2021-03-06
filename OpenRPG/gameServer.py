'''
	This file contains all code related to the games/ directory
'''
from flask import Flask, request, send_from_directory, render_template, url_for, redirect, flash, Blueprint
import json
import os
import shutil
from Game import *
from GamesList import GamesList
from util import *
import glob

GAMES_PATH_BLUEPRINT = Blueprint('GAMES_PATH_BLUEPRINT', __name__, template_folder='../templates/games')

@GAMES_PATH_BLUEPRINT.route('/games')
def showAllGames():
    '''
        List all games
    '''
    return render_template("index.html",
        games=GamesList.getAllGames())

@GAMES_PATH_BLUEPRINT.route('/games/new', methods=['POST'])
def createGame():
    '''
        Create a new game
    '''
    try:
        GamesList.addGame(Game())
    except IOError as e:
        print e
        flash("Something went wrong!")

    flash("Created new game")

    return redirect(url_for('GAMES_PATH_BLUEPRINT.showAllGames'))

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/delete', methods=['POST'])
def deleteGame(gameID):
    '''
        Delete a game
    '''
    try:
        GamesList.removeGame(gameID)
    except IOError as e:
        print e
        flash("Something went wrong!")
    
    return redirect(url_for('GAMES_PATH_BLUEPRINT.showAllGames'))

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/edit')
def editGame(gameID):
    '''
        Edit a game
    '''
    game = GamesList.getByID(gameID)
    
    return render_template("editGame.html",
        game=game,
        tilesets=game.getAllTilesets(),
        levels=game.getAllLevels())

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/setTitle', methods=['POST'])
def setGameTitle(gameID):
    '''
        Sets a game's title
    '''
    title = request.form['gameTitle']
    game = GamesList.getByID(gameID)

    if dirExists(Game.dirFromName(title)):
        flash('Failed to rename game, directory already exists')
    else:
        game.setTitle(title)
        flash('Successfully renamed game')

    return render_template("editGame.html",
        game=game,
        tilesets=game.getAllTilesets(),
        levels=game.getAllLevels())

@GAMES_PATH_BLUEPRINT.route('/games/<path:path>')
def sendGamesFile(path):
    '''
        Send a file from the games directory
    '''
    return send_from_directory('../games', path)

'''
    Tilesets
'''

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/tilesets/add', methods=['POST'])
def addTileset(gameID):
    '''
        Create a tileset
    '''
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
    elif not file.filename.endswith('.png'):
        flash('Upload failed: file type must be .png')
    else:
        directory = GamesList.getByID(gameID).getTileDir()
        destination = os.path.join(directory, file.filename)
        file.save(destination)

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editGame',
        gameID=gameID))

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/tilesets/<string:name>/edit')
def editTileset(gameID, name):
    '''
        Edit a tileset
    '''
    game = GamesList.getByID(gameID)
    tileset = None

    for t in game.getAllTilesets():
        if t.name == name:
            tileset = t
            break

    return render_template('editTileset.html',
        game=game,
        tileset=tileset)

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/tilesets/<string:name>/update', methods=['POST'])
def updateTileset(gameID, name):
    '''
        Update a tileset
    '''
    game = GamesList.getByID(gameID)
    tileset = None

    for t in game.getAllTilesets():
        if t.name == name:
            tileset = t
            break

    # Write values and save
    tileset.tileSize = max(int(request.form['tileSize']), 1)
    tileset.xoff = int(request.form['xoff'])
    tileset.yoff = int(request.form['yoff'])
    tileset.save()

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editTileset',
        gameID=gameID,
        name=name))

'''
    Props
'''

@GAMES_PATH_BLUEPRINT.route('/games/<int:gameID>/props/add', methods=['POST'])
def addProp(gameID):
    '''
        Upload a prop image
    '''
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
    elif not file.filename.endswith('.png'):
        flash('Upload failed: file type must be .png')
    else:
        directory = GamesList.getByID(gameID).getPropDir()
        destination = os.path.join(directory, file.filename)
        file.save(destination)
        flash('Prop added successfully')

    return redirect(url_for('GAMES_PATH_BLUEPRINT.editGame',
        gameID=gameID))
