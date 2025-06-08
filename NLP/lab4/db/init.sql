
CREATE TABLE IF NOT EXISTS input_texts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS predicted_scores (
    id INT PRIMARY KEY,
    text TEXT,
    predicted_score FLOAT
);
