import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Paper,
  CircularProgress,
  FormControlLabel,
  Switch,
  Alert,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { analysisService } from '../services/api';
import toast from 'react-hot-toast';
import SearchIcon from '@mui/icons-material/Search';

const AnalysisPage = () => {
  const navigate = useNavigate();
  const [phoneNumber, setPhoneNumber] = useState('');
  const [deepScan, setDeepScan] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setError('');
    
    // Basic validation
    if (!phoneNumber.trim()) {
      setError('Please enter a phone number');
      return;
    }

    // Phone number format validation (basic)
    if (!phoneNumber.match(/^\+?[1-9]\d{1,14}$/)) {
      setError('Please enter a valid phone number with country code (e.g., +1234567890)');
      return;
    }

    setLoading(true);

    try {
      const result = await analysisService.analyzePhone(phoneNumber, deepScan);
      toast.success('Analysis completed successfully!');
      navigate(`/report/${result.analysis.id}`);
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Analysis failed. Please try again.';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <SearchIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
          <Typography variant="h4" component="h1" gutterBottom>
            Phone Number Analysis
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Enter a phone number to analyze for fraud indicators
          </Typography>
        </Box>

        <Box component="form" onSubmit={handleAnalyze}>
          <TextField
            fullWidth
            label="Phone Number"
            placeholder="+1234567890"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            disabled={loading}
            helperText="Include country code (e.g., +1 for US, +44 for UK)"
            sx={{ mb: 3 }}
          />

          <FormControlLabel
            control={
              <Switch
                checked={deepScan}
                onChange={(e) => setDeepScan(e.target.checked)}
                disabled={loading}
              />
            }
            label="Deep Scan (More comprehensive but takes longer)"
            sx={{ mb: 3 }}
          />

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <Button
            type="submit"
            variant="contained"
            size="large"
            fullWidth
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
          >
            {loading ? 'Analyzing...' : 'Analyze Number'}
          </Button>
        </Box>

        <Box sx={{ mt: 4, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
          <Typography variant="subtitle2" gutterBottom>
            Analysis Includes:
          </Typography>
          <Typography variant="body2" component="ul" sx={{ pl: 2 }}>
            <li>Phone number validation and carrier lookup</li>
            <li>Social media presence scanning</li>
            <li>Spam database checking</li>
            <li>Fraud forum mention detection</li>
            <li>Messaging app presence (Telegram, WhatsApp)</li>
            <li>Risk score calculation with detailed breakdown</li>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default AnalysisPage;
