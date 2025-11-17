import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { analysisService } from '../services/api';
import SecurityIcon from '@mui/icons-material/Security';
import SearchIcon from '@mui/icons-material/Search';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import HistoryIcon from '@mui/icons-material/History';

const HomePage = () => {
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      const data = await analysisService.getStatistics();
      setStatistics(data);
    } catch (error) {
      console.error('Failed to load statistics:', error);
    }
  };

  const features = [
    {
      icon: <SearchIcon sx={{ fontSize: 60 }} />,
      title: 'Phone Number Analysis',
      description: 'Comprehensive OSINT analysis of phone numbers to detect fraud indicators',
    },
    {
      icon: <SecurityIcon sx={{ fontSize: 60 }} />,
      title: 'Risk Assessment',
      description: 'AI-powered risk scoring based on multiple data sources and patterns',
    },
    {
      icon: <AnalyticsIcon sx={{ fontSize: 60 }} />,
      title: 'Detailed Reports',
      description: 'Generate comprehensive reports with evidence and recommendations',
    },
    {
      icon: <HistoryIcon sx={{ fontSize: 60 }} />,
      title: 'Historical Tracking',
      description: 'Track analysis history and identify emerging fraud patterns',
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          OSINT-Based SIM Swap Fraud Detection
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Advanced fraud detection using Open Source Intelligence
        </Typography>
        <Button
          variant="contained"
          size="large"
          component={RouterLink}
          to="/analyze"
          sx={{ mt: 2 }}
        >
          Start Analysis
        </Button>
      </Box>

      {statistics && (
        <Box sx={{ mb: 6 }}>
          <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 3 }}>
            Statistics
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="primary">
                    {statistics.total_analyses}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Analyses
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="error">
                    {statistics.high_risk_count}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    High Risk Detected
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="warning.main">
                    {statistics.medium_risk_count}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Medium Risk
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" color="success.main">
                    {statistics.low_risk_count}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Low Risk
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      )}

      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 3 }}>
          Features
        </Typography>
        <Grid container spacing={3}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card sx={{ height: '100%', textAlign: 'center', p: 2 }}>
                <CardContent>
                  <Box sx={{ color: 'primary.main', mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Box sx={{ textAlign: 'center', p: 4, bgcolor: 'background.paper', borderRadius: 2 }}>
        <Typography variant="h5" gutterBottom>
          ⚠️ Ethical Use Disclaimer
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          This tool is for educational and legitimate fraud prevention purposes only.
          Always obtain proper authorization before investigating phone numbers.
          Respect privacy laws and regulations (GDPR, CCPA, etc.).
        </Typography>
      </Box>
    </Container>
  );
};

export default HomePage;
