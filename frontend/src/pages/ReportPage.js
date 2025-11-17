import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Chip,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  Alert,
} from '@mui/material';
import { useParams } from 'react-router-dom';
import { analysisService } from '../services/api';
import { format } from 'date-fns';
import RiskCard from '../components/RiskCard';
import PhoneIcon from '@mui/icons-material/Phone';
import WarningIcon from '@mui/icons-material/Warning';
import InfoIcon from '@mui/icons-material/Info';

const ReportPage = () => {
  const { id } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadReport = useCallback(async () => {
    try {
      const data = await analysisService.getReport(id);
      setAnalysis(data);
    } catch (err) {
      setError('Failed to load report');
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    loadReport();
  }, [loadReport]);

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'CRITICAL':
      case 'HIGH':
        return 'error';
      case 'MEDIUM':
        return 'warning';
      default:
        return 'info';
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error || !analysis) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error">{error || 'Report not found'}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Fraud Analysis Report
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <RiskCard riskScore={analysis.risk_score} riskLevel={analysis.risk_level} />

          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <PhoneIcon sx={{ mr: 1 }} />
                <Typography variant="h6">Phone Information</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="body2" gutterBottom>
                <strong>Number:</strong> {analysis.phone_number}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Country:</strong> {analysis.country_code || 'Unknown'}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Carrier:</strong> {analysis.carrier || 'Unknown'}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Line Type:</strong> {analysis.line_type || 'Unknown'}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Analysis Date:</strong>{' '}
                {format(new Date(analysis.analysis_date), 'MMM dd, yyyy HH:mm:ss')}
              </Typography>
              <Typography variant="body2">
                <strong>Duration:</strong> {analysis.analysis_duration?.toFixed(2)}s
              </Typography>
            </CardContent>
          </Card>

          {/* Rich Metadata Card */}
          {analysis.rich_metadata && Object.keys(analysis.rich_metadata).length > 0 && (
            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <InfoIcon sx={{ mr: 1 }} />
                  Enhanced Carrier & Location Data
                </Typography>
                <Divider sx={{ mb: 2 }} />

                {/* Carrier Details */}
                {analysis.rich_metadata.carrier_details && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      📡 Carrier Information
                    </Typography>
                    <Box sx={{ ml: 2, mt: 1 }}>
                      <Typography variant="body2">
                        <strong>Current Carrier:</strong> {analysis.rich_metadata.carrier_details.current_carrier || 'Unknown'}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Original Carrier:</strong> {analysis.rich_metadata.carrier_details.original_carrier || 'Unknown'}
                      </Typography>
                      {analysis.rich_metadata.carrier_details.has_been_ported && (
                        <Alert severity="warning" sx={{ mt: 1, mb: 1 }}>
                          ⚠️ Number has been ported from {analysis.rich_metadata.carrier_details.original_carrier} to {analysis.rich_metadata.carrier_details.current_carrier}
                        </Alert>
                      )}
                      <Typography variant="body2">
                        <strong>VOIP:</strong> {analysis.rich_metadata.carrier_details.is_voip ? '✅ Yes' : '❌ No'}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Prepaid:</strong> {
                          analysis.rich_metadata.carrier_details.is_prepaid === null 
                            ? '❔ Unknown (Likely prepaid in this region)' 
                            : analysis.rich_metadata.carrier_details.is_prepaid 
                              ? '✅ Yes' 
                              : '❌ No'
                        }
                      </Typography>
                      <Typography variant="body2">
                        <strong>Line Type:</strong> {analysis.rich_metadata.carrier_details.line_type || 'Unknown'}
                      </Typography>
                    </Box>
                  </Box>
                )}

                {/* Geographic Data */}
                {analysis.rich_metadata.geographic_data && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      🌍 Geographic Location
                    </Typography>
                    <Box sx={{ ml: 2, mt: 1 }}>
                      <Typography variant="body2">
                        <strong>Country:</strong> {analysis.rich_metadata.geographic_data.country || 'Unknown'}
                      </Typography>
                      <Typography variant="body2">
                        <strong>City:</strong> {analysis.rich_metadata.geographic_data.city || 'Unknown'}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Region:</strong> {analysis.rich_metadata.geographic_data.region || 'Unknown'}
                      </Typography>
                      <Typography variant="body2">
                        <strong>Timezone:</strong> {analysis.rich_metadata.geographic_data.timezone || 'Unknown'}
                      </Typography>
                    </Box>
                  </Box>
                )}

                {/* Number Status */}
                {analysis.rich_metadata.number_status && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      📊 Number Status
                    </Typography>
                    <Box sx={{ ml: 2, mt: 1 }}>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 1 }}>
                        <Chip 
                          label={analysis.rich_metadata.number_status.active ? '✅ Active' : '❌ Inactive'} 
                          color={analysis.rich_metadata.number_status.active ? 'success' : 'error'}
                          size="small"
                        />
                        <Chip 
                          label={analysis.rich_metadata.number_status.valid ? '✅ Valid' : '❌ Invalid'} 
                          color={analysis.rich_metadata.number_status.valid ? 'success' : 'error'}
                          size="small"
                        />
                        {analysis.rich_metadata.number_status.risky && (
                          <Chip label="⚠️ Risky" color="warning" size="small" />
                        )}
                        {analysis.rich_metadata.number_status.do_not_call && (
                          <Chip label="🚫 Do Not Call" color="error" size="small" />
                        )}
                      </Box>
                    </Box>
                  </Box>
                )}

                {/* Reputation Indicators */}
                {analysis.rich_metadata.reputation_indicators && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      🎯 Reputation Metrics
                    </Typography>
                    <Box sx={{ ml: 2, mt: 1 }}>
                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Fraud Score:</strong> {analysis.rich_metadata.reputation_indicators.fraud_score}/100
                      </Typography>
                      <Box sx={{ 
                        width: '100%', 
                        height: 20, 
                        bgcolor: 'grey.200', 
                        borderRadius: 1,
                        overflow: 'hidden',
                        mb: 2
                      }}>
                        <Box sx={{
                          width: `${analysis.rich_metadata.reputation_indicators.fraud_score}%`,
                          height: '100%',
                          bgcolor: analysis.rich_metadata.reputation_indicators.fraud_score > 75 ? 'error.main' : 
                                  analysis.rich_metadata.reputation_indicators.fraud_score > 50 ? 'warning.main' : 'success.main',
                          transition: 'width 0.3s ease'
                        }} />
                      </Box>
                      <Typography variant="body2">
                        <strong>Spam Score:</strong> {analysis.rich_metadata.reputation_indicators.spam_score}/100
                      </Typography>
                      {analysis.rich_metadata.reputation_indicators.recent_abuse && (
                        <Alert severity="error" sx={{ mt: 1 }}>
                          ⚠️ Recent abuse detected for this number
                        </Alert>
                      )}
                    </Box>
                  </Box>
                )}

                {/* Number Age */}
                {analysis.rich_metadata.number_age && (
                  <Box>
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      ⏰ Number Age Estimation
                    </Typography>
                    <Box sx={{ ml: 2, mt: 1 }}>
                      <Chip 
                        label={analysis.rich_metadata.number_age}
                        color="info"
                        size="small"
                      />
                    </Box>
                  </Box>
                )}
              </CardContent>
            </Card>
          )}
        </Grid>

        <Grid item xs={12} md={8}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <WarningIcon sx={{ mr: 1 }} />
                <Typography variant="h6">Risk Factors</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />
              {analysis.risk_factors && analysis.risk_factors.length > 0 ? (
                <List>
                  {analysis.risk_factors.map((factor, index) => (
                    <ListItem key={index} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                      <Box sx={{ width: '100%', display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="subtitle1">{factor.factor_type}</Typography>
                        <Chip
                          label={factor.severity}
                          color={getSeverityColor(factor.severity)}
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        {factor.description}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 1 }}>
                        Source: {factor.source} | Contribution: {factor.score_contribution}
                      </Typography>
                      <Divider sx={{ width: '100%', mt: 2 }} />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Alert severity="success">No significant risk factors detected</Alert>
              )}
            </CardContent>
          </Card>

          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <InfoIcon sx={{ mr: 1 }} />
                <Typography variant="h6">Social Media & Online Presence</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />

              <Alert severity="info" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  <strong>Privacy Notice:</strong> Only publicly accessible information is displayed. 
                  Private account data and login credentials are never accessible or displayed.
                </Typography>
              </Alert>

              <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold', mt: 2 }}>
                📱 Platforms Checked
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                {analysis.social_media_presence?.platforms_checked && analysis.social_media_presence.platforms_checked.length > 0 ? (
                  analysis.social_media_presence.platforms_checked.map((platform, index) => (
                    <Chip key={index} label={platform} size="small" color="default" />
                  ))
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No platforms were scanned for this number
                  </Typography>
                )}
              </Box>

              <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold' }}>
                🔍 Public Profile Matches
              </Typography>
              <Typography variant="body2" paragraph>
                {analysis.social_media_presence?.total_accounts || 0} public profile(s) found where this phone number is listed
                {analysis.social_media_presence?.total_accounts > 0 && (
                  <Typography variant="caption" display="block" sx={{ mt: 1, fontStyle: 'italic' }}>
                    Note: These are only publicly accessible profiles where the owner has chosen to share their phone number
                  </Typography>
                )}
              </Typography>

              {analysis.social_media_presence?.public_profiles_found?.length > 0 && (
                <Box sx={{ ml: 2, mb: 2 }}>
                  {analysis.social_media_presence.public_profiles_found.map((profile, index) => (
                    <Box key={index} sx={{ mb: 1, p: 1, bgcolor: 'background.default', borderRadius: 1 }}>
                      <Typography variant="body2"><strong>{profile.platform}:</strong> {profile.name}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        Type: {profile.profile_type} | Verified: {profile.verified ? 'Yes' : 'No'}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              )}

              <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold', color: 'warning.main' }}>
                ⚠️ Data Breach Appearances
              </Typography>
              <Typography variant="body2" paragraph>
                {analysis.social_media_presence?.breach_count || 0} known data breach(es) containing this phone number
                {(analysis.social_media_presence?.breach_count > 0) && (
                  <Alert severity="warning" sx={{ mt: 1 }}>
                    This phone number appears in {analysis.social_media_presence.breach_count} known data breach(es). 
                    Consider this number compromised.
                  </Alert>
                )}
              </Typography>
            </CardContent>
          </Card>

          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <InfoIcon sx={{ mr: 1 }} />
                <Typography variant="h6">Additional OSINT Findings</Typography>
              </Box>
              <Divider sx={{ mb: 2 }} />

              <Typography variant="subtitle2" gutterBottom>
                Spam Reports
              </Typography>
              <Typography variant="body2" paragraph>
                {analysis.spam_reports_count} report(s) found in spam databases
              </Typography>

              <Typography variant="subtitle2" gutterBottom>
                Fraud Forum Mentions
              </Typography>
              <Typography variant="body2" paragraph>
                {analysis.fraud_mentions_count} mention(s) in fraud-related forums
              </Typography>

              <Typography variant="subtitle2" gutterBottom>
                Data Sources Used
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {analysis.data_sources_used?.map((source, index) => (
                  <Chip key={index} label={source} size="small" />
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ReportPage;
