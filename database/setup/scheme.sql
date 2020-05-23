CREATE TABLE users
(
    id       INTEGER PRIMARY KEY,
    name          TEXT    NOT NULL,
    password_hash TEXT NOT NULL,
    creation      INTEGER NOT NULL,
    last_login    INTEGER DEFAULT NULL,
    last_write    INTEGER NOT NULL
);

CREATE TABLE messages
(
    id         INTEGER PRIMARY KEY,
    sender             INTEGER NOT NULL,
    receiver           INTEGER NOT NULL,
    text_content       TEXT CHECK (additional_content NOT NULL OR
                                   text_content NOT NULL),
    additional_content INTEGER DEFAULT NULL,
    creation           INTEGER NOT NULL,
    date_sent          INTEGER NOT NULL,
    date_delivered     INTEGER,
    date_read          INTEGER,
    last_write         INTEGER NOT NULL,

    FOREIGN KEY (sender) REFERENCES users (id),
    FOREIGN KEY (receiver) REFERENCES users (id),
    FOREIGN KEY (additional_content) REFERENCES blobs (id)
);

CREATE TABLE message_history
(
    id        INTEGER PRIMARY KEY,
    for_message     INTEGER NOT NULL,
    from_text       TEXT    DEFAULT NULL CHECK (from_text NOT NULL OR
                                                from_additional NOT NULL),
    from_additional INTEGER DEFAULT NULL,
    creation        INTEGER NOT NULL,

    FOREIGN KEY (for_message) REFERENCES messages (id),
    FOREIGN KEY (from_additional) REFERENCES blobs (id)
);

CREATE TABLE blobs
(
    id  INTEGER PRIMARY KEY,
    type     INTEGER CHECK (type BETWEEN 1 AND 2),
    fs_path  TEXT    NOT NULL,
    author   INTEGER NOT NULL,
    hash     TEXT    NOT NULL,
    creation INTEGER NOT NULL,

    FOREIGN KEY (author) REFERENCES users (id)
)