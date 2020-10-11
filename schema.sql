CREATE TABLE Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE Rooms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    owner INTEGER NOT NULL,
    
    CONSTRAINT owner_room
        FOREIGN KEY (owner)
        REFERENCES Users(id)
);

CREATE TABLE RoomUserRelation(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user INTEGER NOT NULL,
    room INTEGER NOT NULL,
    
    CONSTRAINT u_rel
        FOREIGN KEY (user)
        REFERENCES Users(id)

    CONSTRAINT r_rel
        FOREIGN KEY (room)
        REFERENCES Rooms(id)
);

CREATE TABLE Messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    by_user INTEGER NOT NULL,
    body TEXT NOT NULL,
    time TEXT NOT NULL,
    room INTEGER NOT NULL,

    CONSTRAINT user_message
        FOREIGN KEY (by_user)
        REFERENCES Users(id)

    CONSTRAINT room_message
        FOREIGN KEY (room)
        REFERENCES Rooms(id)
);