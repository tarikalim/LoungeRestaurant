import React from 'react';
import {FormControl, InputLabel, Select, MenuItem} from '@mui/material';

const FilterSelector = ({sentiment, onChange}) => {
    const handleChange = (event) => {
        onChange(event.target.value);
    };

    return (
        <FormControl variant="outlined" size="small" sx={{minWidth: 120}}>
            <InputLabel id="sentiment-select-label">Sentiment</InputLabel>
            <Select
                labelId="sentiment-select-label"
                id="sentiment-select"
                value={sentiment}
                onChange={handleChange}
                label="Sentiment"
            >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="positive">Positive</MenuItem>
                <MenuItem value="neutral">Neutral</MenuItem>
                <MenuItem value="negative">Negative</MenuItem>
            </Select>
        </FormControl>
    );
};

export default FilterSelector;
