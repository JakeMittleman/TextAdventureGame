import stdio
import random
import sys

# Weapon Stats
weapon = {'bone base':4, 'bone max':9, 'none base':2, 'none max':4}

# Player Stats
player = {'weapon':'None', 'Health':20, 'Holding':'None'}

# enemy
giant_rat = {'name':'Giant Rat', 'Health':15, 'attack low':1, 'attack high':4}

giant_spider = {'name':'Giant Spider', 'Health':20,
                'attack low':3, 'attack high':7}

# ------------------------

# ROOMS/EVENTS

cell = {
    'name':'cell',
    'desc':'You awake to find yourself in a cell. ' +
           'You\'re not sure how or why you\'re here, ' +
           'but you need to escape. Do you want to ' +
           'look around?',
    'actions':{'yes':'cell_exam', 'no':'cell'}
    }

cell_exam = {
    'name':'cell_exam',
    'desc':'You look around the cell. You see ' +
           'an old bone lying in the corner of the room. The cell ' +
           'has a gate that looks like the exit. Next to you ' +
           'is a dusty pillow.',
    'actions':{'bone':'bone_exam', 'pillow':'pillow_exam', 'door':'door_exam'}
    }

pillow_exam = {
    'name':'pillow_exam',
    'desc':'You notice something strange about ' +
           'the dusty pillow lying on the cot. ' +
           'You lift the pillow and cough as dust fills the air. ' +
           'As the dust clears, you see a corroded key underneath ' +
           'the pillow. You hastily pick it up and shove it in your pocket.',
    'actions':{'bone':'bone_exam', 'door':'door_exam', 'cell':'cell_exam'}
    }

bone_exam = {
    'name':'bone_exam',
    'desc':'You walk over to the old bone lying in the corner.' +
           'You take it in your hands and you notice it has some weight.' +
           ' Do you want to take it?',
    'actions':{'yes':'bone_take', 'no':'cell_exam'}
    }

bone_take = {
    'name':'bone_take',
    'desc':'You take the bone.',
    'actions':{'cell':'cell_exam', 'pillow':'pillow_exam',
               'door':'door_exam'},
    'taken':False
    }

door_exam = {
    'name':'door_exam',
    'desc':'You rush over to the door and grasp the metal ' +
           'cast iron handle. You furiously shake the door ' +
           'as hard as you can. The door rattles but is firmly ' +
           'locked.',
    'desc2':'Your hand sweating, you slowly push the key into ' +
            'the lock. You turn it and hear the door click.' +
            ' You pull the door open and step into the dark hallway.',
    'actions':{'pillow':'pillow_exam', 'bone':'bone_exam',
               'cell':'cell_exam'},
    'exit':False
    }

map = dict( (item['name'], item) for item in (cell, cell_exam, bone_exam,
                                              pillow_exam, bone_take,
                                              door_exam) )

PROMPT = '> '

def gameLoop(currentRoom = map['cell']):

    userInput = stdio.readString()

    if userInput in currentRoom['actions']:
        currentRoom = map[currentRoom['actions'][userInput]]

        if userInput == 'door' and player['Holding'] == 'key':
            stdio.writeln('\n' + door_exam['desc2'])
            battleLoop()

        if currentRoom == 'bone_take':
            bone_take['taken'] = True
        
    else:
        stdio.writeln()
        stdio.writeln('Sorry, that\'s not a valid input. Try Again.\n')
        stdio.write(PROMPT)
        gameLoop(currentRoom)

    if bone_take['taken'] == True:
        player['weapon'] = 'bone'

    stdio.writeln()
    keyCheck(currentRoom)
    stdio.writeln(currentRoom['desc'])
    stdio.writeln()
    actionList(currentRoom)
    stdio.writeln()
    stdio.write(PROMPT)

    gameLoop(currentRoom)

def actionList(currentRoom = map['cell']):

    stdio.writeln('What would you like to do? Here are your options:\n')
    for item in currentRoom['actions']:
        stdio.write(str(item) + ' ' + '/' + ' ')

    stdio.writeln()

def keyCheck(currentRoom = map['cell']):

    if currentRoom == pillow_exam:
        if player['Holding'] == 'key':
            stdio.writeln('You\'ve already taken the key. ' +
                          'There is nothing else to take.')
            stdio.writeln()
            actionList(currentRoom)
            stdio.writeln()
            stdio.write(PROMPT)
            gameLoop(currentRoom)

    if currentRoom == pillow_exam:
        if player['Holding'] != 'key':
            player['Holding'] = 'key'

def attackLoop(enemy):
        
    stdio.writeln('What do you want to do?')
    stdio.writeln('\nattack / run\n')

    stdio.write(PROMPT)
    battleInput = stdio.readString()

    if battleInput == 'attack':
        if player['weapon'] == 'bone':
            atkDmg = random.randrange(weapon['bone base'],
                                      weapon['bone max'] + 1)
            enemy['Health'] -= atkDmg
            stdio.writef('\nYou strike the beast for %d damage.\n', atkDmg)

        else:
            atkDmg = random.randrange(weapon['none base'],
                                      weapon['none max']+1)
            enemy['Health'] -= atkDmg
            stdio.writef('\nYou strike the beast for %d damage.\n', atkDmg)

        if enemy['Health'] <= 0:
            stdio.writeln('The beast is dead. You catch your ' +
                          'breath and step over the body using ' +
                          'the walls as support. You slowly make ' +
                          'your way down the corridor until you\'re ' +
                          'blinded by sunlight. You\'ve escaped. ' +
                          'Good job!')
            stdio.writeln('\nPlay Again?\n')
            stdio.writeln('\nyes / no\n')
            stdio.write(PROMPT)
            tryAgain = stdio.readString()
            if tryAgain == 'yes':
                gameLoop()

            else:
                sys.exit()

    elif battleInput == 'run':
        escapeChance = random.randrange(1, 101)
        if escapeChance >= 80:
            stdio.writeln('\nYou make a dash down the hall ' +
                          'and don\'t stop running until you feel ' +
                          'the sunshine on your face. You\'ve done it.' +
                          ' You\'ve escaped. Good Job!')
            stdio.writeln('\nPlay Again?\n')
            stdio.writeln('\nyes / no\n')
            stdio.write(PROMPT)
            tryAgain = stdio.readString()

            if tryAgain == 'yes':
                main()

            elif tryAgain == 'no':
                sys.exit()

        else:
            stdio.writeln('\nYou try to escape but the ' + str(enemy['name'])
                          + ' catches you.')

    else:
        stdio.writeln('\nSorry, that\'s not a valid command')
        attackLoop(enemy)

    hurtDmg = random.randrange(enemy['attack low'], enemy['attack high'] + 1)
    player['Health'] -= hurtDmg
    stdio.writef('\nThe beast strikes you for %d damage.\n\n', hurtDmg)

    if player['Health'] <= 0:
        stdio.writeln('Alas, the beast has struck you down.' +
                      ' You\'ve failed to escape. Try again?')
        stdio.writeln('\nyes / no\n')
        stdio.write(PROMPT)

        tryAgain = stdio.readString()

        if tryAgain == 'yes':
            main()

        elif tryAgain == 'no':
            sys.exit()

    attackLoop(enemy)

def battleLoop():

    enemyList = [giant_rat, giant_spider]
    enemy = enemyList[random.randrange(2)]
    stdio.writeln('Suddenly a ' + enemy['name'] + ' appears!')
    attackLoop(enemy)

def main():

    stdio.writeln()
    stdio.writeln(cell['desc'])
    stdio.writeln()
    stdio.writeln('yes / no\n')
    stdio.write(PROMPT)
    gameLoop()

if __name__ == '__main__':
    main()
