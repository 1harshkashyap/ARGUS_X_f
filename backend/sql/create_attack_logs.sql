CREATE TABLE IF NOT EXISTS attack_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    input_text TEXT,
    allowed BOOLEAN,
    fingerprint TEXT,
    threat_score INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
