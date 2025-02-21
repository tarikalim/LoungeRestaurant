import React, { useState, useEffect, useMemo } from 'react';
import { Container, Box, Pagination, AppBar, Toolbar, Typography, Paper, Table, TableContainer, TableHead, TableRow, TableCell, TableBody } from '@mui/material';
import FilterSelector from '../component/FilterSelector';
import { getComments } from '../api/comment';

const CommentPage = () => {
    const [allComments, setAllComments] = useState([]);
    const [totalComments, setTotalComments] = useState(0);
    const [sentiment, setSentiment] = useState('');
    const [page, setPage] = useState(1);
    const pageSize = 10;

    const fetchComments = async () => {
        try {
            const data = await getComments(sentiment);
            setAllComments(data.comments);
            setTotalComments(data.total);
        } catch (error) {
            console.error('Error fetching comments:', error);
        }
    };

    useEffect(() => {
        setPage(1);
        fetchComments();
    }, [sentiment]);

    useEffect(() => {
        fetchComments();
    }, []);

    const paginatedComments = useMemo(() => {
        const startIndex = (page - 1) * pageSize;
        return allComments.slice(startIndex, startIndex + pageSize);
    }, [allComments, page]);

    const handleSentimentChange = (newSentiment) => {
        setSentiment(newSentiment);
    };

    const handlePageChange = (event, value) => {
        setPage(value);
    };

    return (
        <Container>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6">Comments</Typography>
                    <Box sx={{ marginLeft: 'auto' }}>
                        <FilterSelector sentiment={sentiment} onChange={handleSentimentChange} />
                    </Box>
                </Toolbar>
            </AppBar>

            <Box sx={{ marginTop: 2 }}>
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>ID</TableCell>
                                <TableCell>Content</TableCell>
                                <TableCell>Sentiment</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {paginatedComments.map((comment) => (
                                <TableRow key={comment.id}>
                                    <TableCell>{comment.id}</TableCell>
                                    <TableCell>{comment.content}</TableCell>
                                    <TableCell>{comment.sentiment}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Box>

            <Box sx={{ marginTop: 2, display: 'flex', justifyContent: 'center' }}>
                <Pagination
                    count={Math.ceil(totalComments / pageSize)}
                    page={page}
                    onChange={handlePageChange}
                    color="primary"
                />
            </Box>
        </Container>
    );
};

export default CommentPage;
