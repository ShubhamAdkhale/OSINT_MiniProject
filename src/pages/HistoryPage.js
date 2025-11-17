import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Button,
  TextField,
  MenuItem,
  CircularProgress,
  Pagination,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { analysisService } from '../services/api';
import { format } from 'date-fns';
import { utcToZonedTime } from 'date-fns-tz';
import toast from 'react-hot-toast';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';

const HistoryPage = () => {
  const navigate = useNavigate();
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchPhone, setSearchPhone] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deleteAllDialogOpen, setDeleteAllDialogOpen] = useState(false);
  const [selectedAnalysisId, setSelectedAnalysisId] = useState(null);

  const loadHistory = useCallback(async () => {
    setLoading(true);
    try {
      const data = await analysisService.getHistory(page, 10);
      setAnalyses(data.analyses);
      setTotalPages(data.pages);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setLoading(false);
    }
  }, [page]);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await analysisService.searchAnalyses(searchPhone, riskFilter);
      setAnalyses(data.analyses);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSearchPhone('');
    setRiskFilter('');
    setPage(1);
    loadHistory();
  };

  const handleDeleteClick = (analysisId) => {
    setSelectedAnalysisId(analysisId);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    try {
      await analysisService.deleteAnalysis(selectedAnalysisId);
      toast.success('Analysis deleted successfully');
      setDeleteDialogOpen(false);
      setSelectedAnalysisId(null);
      loadHistory();
    } catch (error) {
      toast.error('Failed to delete analysis');
      console.error('Delete failed:', error);
    }
  };

  const handleClearAllClick = () => {
    setDeleteAllDialogOpen(true);
  };

  const handleClearAllConfirm = async () => {
    try {
      await analysisService.clearAllHistory();
      toast.success('All history cleared successfully');
      setDeleteAllDialogOpen(false);
      loadHistory();
    } catch (error) {
      toast.error('Failed to clear history');
      console.error('Clear all failed:', error);
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'HIGH':
      case 'CRITICAL':
        return 'error';
      case 'MEDIUM':
        return 'warning';
      case 'LOW':
        return 'info';
      default:
        return 'success';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Analysis History
        </Typography>
        {analyses.length > 0 && (
          <Button
            variant="outlined"
            color="error"
            startIcon={<DeleteSweepIcon />}
            onClick={handleClearAllClick}
          >
            Clear All
          </Button>
        )}
      </Box>

      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            label="Search Phone Number"
            value={searchPhone}
            onChange={(e) => setSearchPhone(e.target.value)}
            size="small"
            sx={{ flex: 1 }}
          />
          <TextField
            select
            label="Risk Level"
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            size="small"
            sx={{ minWidth: 150 }}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="HIGH">High</MenuItem>
            <MenuItem value="MEDIUM">Medium</MenuItem>
            <MenuItem value="LOW">Low</MenuItem>
            <MenuItem value="MINIMAL">Minimal</MenuItem>
          </TextField>
          <Button variant="contained" onClick={handleSearch}>
            Search
          </Button>
          <Button variant="outlined" onClick={handleReset}>
            Reset
          </Button>
        </Box>
      </Paper>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Phone Number</TableCell>
                  <TableCell>Risk Score</TableCell>
                  <TableCell>Risk Level</TableCell>
                  <TableCell>Carrier</TableCell>
                  <TableCell>Analysis Date</TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {analyses.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      No analyses found
                    </TableCell>
                  </TableRow>
                ) : (
                  analyses.map((analysis) => (
                    <TableRow key={analysis.id} hover>
                      <TableCell>{analysis.phone_number}</TableCell>
                      <TableCell>{analysis.risk_score}</TableCell>
                      <TableCell>
                        <Chip
                          label={analysis.risk_level}
                          color={getRiskColor(analysis.risk_level)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{analysis.carrier || 'Unknown'}</TableCell>
                      <TableCell>
                        {format(utcToZonedTime(new Date(analysis.analysis_date), 'Asia/Kolkata'), 'MMM dd, yyyy hh:mm a')}
                      </TableCell>
                      <TableCell align="center">
                        <Button
                          size="small"
                          startIcon={<VisibilityIcon />}
                          onClick={() => navigate(`/report/${analysis.id}`)}
                          sx={{ mr: 1 }}
                        >
                          View
                        </Button>
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteClick(analysis.id)}
                          title="Delete"
                        >
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>

          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={(e, value) => setPage(value)}
                color="primary"
              />
            </Box>
          )}
        </>
      )}

      {/* Delete Single Analysis Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this analysis? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Clear All History Dialog */}
      <Dialog
        open={deleteAllDialogOpen}
        onClose={() => setDeleteAllDialogOpen(false)}
      >
        <DialogTitle>Clear All History</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete ALL analysis history? This will permanently delete all records and cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteAllDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleClearAllConfirm} color="error" variant="contained">
            Clear All
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default HistoryPage;
