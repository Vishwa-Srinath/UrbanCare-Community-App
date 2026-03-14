CREATE TABLE citizens (
    -- Links directly to the user_id in the users table
    user_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    
    phone_number VARCHAR(15),
    address TEXT,
    date_of_birth DATE,
    
    -- Ensuring tracking columns are present for the profile too
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER set_citizens_updated_at
BEFORE UPDATE ON citizens
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

