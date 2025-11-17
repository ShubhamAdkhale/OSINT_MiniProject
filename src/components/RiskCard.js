import React from 'react';
import { Card, CardContent, Typography, Chip, Box } from '@mui/material';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';

const RiskCard = ({ riskScore, riskLevel }) => {
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

  const getRiskIcon = (level) => {
    switch (level) {
      case 'HIGH':
      case 'CRITICAL':
        return <ErrorIcon />;
      case 'MEDIUM':
        return <WarningIcon />;
      default:
        return <CheckCircleIcon />;
    }
  };

  return (
    <Card sx={{ minWidth: 275, mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5" component="div">
            Risk Assessment
          </Typography>
          <Chip
            icon={getRiskIcon(riskLevel)}
            label={riskLevel}
            color={getRiskColor(riskLevel)}
          />
        </Box>
        <Box sx={{ mt: 2 }}>
          <Typography variant="h2" color="text.secondary" sx={{ textAlign: 'center' }}>
            {riskScore}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center' }}>
            Risk Score (0-100)
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default RiskCard;
