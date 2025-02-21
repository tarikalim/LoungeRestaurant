import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const CommentCard = ({ comment }) => {
    return (
        <Card variant="outlined">
            <CardContent>
                <Typography variant="body1">
                    {comment.content}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                    Sentiment: {comment.sentiment}
                </Typography>
            </CardContent>
        </Card>
    );
};

export default CommentCard;
