-- =====================================================
-- BEHAVIORAL PROFILES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS behavioral_profiles (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL REFERENCES users(id),

    phenotype VARCHAR(100) NOT NULL,

    risk_score FLOAT NOT NULL,
    confidence FLOAT NOT NULL,

    stability_score FLOAT,
    adherence_score FLOAT,
    stress_index FLOAT,
    lifestyle_score FLOAT,

    model_version VARCHAR(50),

    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- BEHAVIORAL PROFILE HISTORY (LONGITUDINAL TRACKING)
-- =====================================================

CREATE TABLE IF NOT EXISTS behavioral_profile_history (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    profile_id INTEGER REFERENCES behavioral_profiles(id),

    phenotype VARCHAR(100),

    snapshot JSONB NOT NULL,

    created_at TIMESTAMP DEFAULT NOW()
);

-- INDEXES (IMPORTANT FOR SCALABILITY)

CREATE INDEX idx_behavioral_profiles_user
ON behavioral_profiles(user_id);

CREATE INDEX idx_behavioral_history_user
ON behavioral_profile_history(user_id);