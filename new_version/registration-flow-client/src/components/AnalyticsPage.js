// new_version/registration-flow-client/src/components/AnalyticsLogsPage.js
// Wide-format logs dashboard showing all registration sessions in a detailed table

import React, { useState, useEffect } from "react";
import styles from "./AnalyticsPage.module.css";
import { analyticsService } from "../api/analyticsService";
import { getOrCreateSessionId } from "../utils/sessionManager";

const AnalyticsLogsPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [steps, setSteps] = useState([]);
  
  // Pagination
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  
  // Filters
  const [statusFilter, setStatusFilter] = useState('all');
  const [stepFilter, setStepFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('📊 Loading analytics logs...');
      
      const [stepsData, statsData] = await Promise.all([
        analyticsService.getRegistrationSteps(),
        analyticsService.getRegistrationStats(),
      ]);

      setSteps(stepsData);
      setStats(statsData);
      
      // Load actual session data
      await loadSessionsData();
      
      console.log('✅ Analytics logs loaded successfully');
      
    } catch (err) {
      console.error('❌ Error loading analytics:', err);
      setError(`Failed to load analytics: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

    const loadSessionsData = async () => {
    try {
        // Add this method to your analyticsService.js:
        const sessionsData = await analyticsService.getAllSessions();
        setSessions(sessionsData);
    } catch (err) {
        console.error('Error loading sessions:', err);
        setSessions([]);
    }
    };


  const getStepName = (stepId) => {
    const step = steps.find(s => s.id === stepId);
    return step ? step.step_name : 'Unknown';
  };

  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return '-';
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDuration = (seconds) => {
    if (!seconds || seconds < 0) return '-';
    
    if (seconds < 60) return `${Math.round(seconds)}s`;
    
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.round(seconds % 60);
    
    if (minutes < 60) {
      return `${minutes}m ${remainingSeconds}s`;
    }
    
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    return `${hours}h ${remainingMinutes}m`;
  };

  const getStatusChip = (status) => {
    const statusConfig = {
      completed: { label: 'Completed', className: styles.chipSuccess, icon: '✓' },
      in_progress: { label: 'In Progress', className: styles.chipPrimary, icon: '⏳' },
      abandoned: { label: 'Abandoned', className: styles.chipWarning, icon: '⚠' }
    };
    
    const config = statusConfig[status] || statusConfig.abandoned;
    
    return (
      <span className={`${styles.chip} ${config.className}`}>
        {config.icon} {config.label}
      </span>
    );
  };

  const exportToCSV = () => {
    console.log('Exporting to CSV...');
    
    const headers = [
      'Session ID',
      'User ID',
      'User Email',
      'Status',
      'Current Step',
      'Steps Completed',
      'Started At',
      'Last Activity',
      'Duration'
    ];
    
    let csvContent = headers.join(',') + '\n';
    
    const filteredSessions = getFilteredSessions();
    filteredSessions.forEach(session => {
      const row = [
        `"${session.session_id}"`,
        session.user_id || 'Anonymous',
        session.user_email || 'N/A',
        session.status,
        `"${session.current_step}"`,
        session.steps_completed,
        `"${session.started_at}"`,
        `"${session.last_activity}"`,
        session.duration_seconds
      ];
      csvContent += row.join(',') + '\n';
    });
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `analytics_logs_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  const getFilteredSessions = () => {
    let filtered = [...sessions];
    
    if (statusFilter !== 'all') {
      filtered = filtered.filter(s => s.status === statusFilter);
    }
    
    if (stepFilter !== 'all') {
      filtered = filtered.filter(s => s.current_step_code === parseInt(stepFilter));
    }
    
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(s => 
        s.session_id.toLowerCase().includes(term) ||
        s.user_id?.toLowerCase().includes(term) ||
        s.user_email?.toLowerCase().includes(term)
      );
    }
    
    return filtered;
  };

  const paginatedSessions = getFilteredSessions().slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  const handleChangePage = (newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (e) => {
    setRowsPerPage(parseInt(e.target.value, 10));
    setPage(0);
  };

  const clearFilters = () => {
    setSearchTerm('');
    setStatusFilter('all');
    setStepFilter('all');
    setPage(0);
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loadingContainer}>
          <div style={{ fontSize: '48px' }}>⏳</div>
          <h2 style={{ color: 'white', marginTop: '16px' }}>Loading Analytics Logs...</h2>
        </div>
      </div>
    );
  }

  const filteredSessions = getFilteredSessions();
  const totalPages = Math.ceil(filteredSessions.length / rowsPerPage);

  return (
    <div className={styles.container}>
      {/* Header */}
      <div className={styles.header}>
        <h1 className={styles.title}>
          📊 Registration Logs
        </h1>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button 
            className={styles.refreshButton}
            onClick={exportToCSV}
            title="Export to CSV"
          >
            <span className={styles.refreshIcon}>💾</span>
          </button>
          <button 
            className={styles.refreshButton}
            onClick={loadAnalyticsData}
            disabled={loading}
            title="Refresh Data"
          >
            <span className={styles.refreshIcon}>🔄</span>
          </button>
        </div>
      </div>

      {error && (
        <div className={styles.alert} style={{ background: '#fee', color: '#c33' }}>
          ⚠️ {error}
        </div>
      )}

      {/* Statistics Cards */}
      {stats && (
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Total Sessions</div>
            <div className={styles.statValue}>{stats.total_sessions || 0}</div>
          </div>
          
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Completed</div>
            <div className={styles.statValue} style={{ color: '#2e7d32' }}>
              {stats.completed_registrations || 0}
            </div>
          </div>
          
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Incomplete</div>
            <div className={styles.statValue} style={{ color: '#e65100' }}>
              {stats.incomplete_registrations || 0}
            </div>
          </div>
          
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Success Rate</div>
            <div className={styles.statValue}>
              {stats.completion_rate ? `${stats.completion_rate.toFixed(1)}%` : '0%'}
            </div>
            <div style={{ 
              width: '100%', 
              height: '6px', 
              background: '#e0e0e0', 
              borderRadius: '3px',
              marginTop: '12px',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${stats.completion_rate || 0}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #667eea, #764ba2)',
                transition: 'width 0.3s ease'
              }} />
            </div>
          </div>
        </div>
      )}

      {/* Filters Section */}
      <div className={styles.searchSection}>
        <h2 className={styles.searchTitle}>🔍 Filters & Search</h2>
        <div className={styles.divider} />
        
        <div className={styles.searchGrid}>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="Search by Session ID, User ID, or Email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              padding: '12px 16px',
              fontSize: '16px',
              border: '2px solid #e0e0e0',
              borderRadius: '12px',
              outline: 'none',
              transition: 'border-color 0.2s'
            }}
            onFocus={(e) => e.target.style.borderColor = '#667eea'}
            onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
          />
          
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            style={{
              padding: '12px 16px',
              fontSize: '16px',
              border: '2px solid #e0e0e0',
              borderRadius: '12px',
              outline: 'none',
              cursor: 'pointer'
            }}
          >
            <option value="all">All Statuses</option>
            <option value="completed">Completed</option>
            <option value="in_progress">In Progress</option>
            <option value="abandoned">Abandoned</option>
          </select>
          
          <select
            value={stepFilter}
            onChange={(e) => setStepFilter(e.target.value)}
            style={{
              padding: '12px 16px',
              fontSize: '16px',
              border: '2px solid #e0e0e0',
              borderRadius: '12px',
              outline: 'none',
              cursor: 'pointer'
            }}
          >
            <option value="all">All Steps</option>
            {steps.map(step => (
              <option key={step.code} value={step.code.toString()}>
                {step.code}. {step.step_name}
              </option>
            ))}
          </select>
          
          <button
            className={styles.searchButton}
            onClick={clearFilters}
            style={{ background: 'linear-gradient(135deg, #e0e0e0, #bdbdbd)', color: '#333' }}
          >
            Clear Filters
          </button>
        </div>
        
        <div style={{ marginTop: '16px', color: '#666', fontSize: '14px' }}>
          Showing {filteredSessions.length} of {sessions.length} sessions
        </div>
      </div>

      {/* Sessions Table */}
      {paginatedSessions.length > 0 ? (
        <div className={styles.tableContainer}>
          <div style={{ overflowX: 'auto' }}>
            <table className={styles.table} style={{ minWidth: '1400px' }}>
              <thead className={styles.tableHead}>
                <tr>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '200px' }}>Session ID</th>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '150px' }}>User ID</th>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '140px' }}>Status</th>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '180px' }}>Current Step</th>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '100px' }}>Progress</th>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '180px' }}>Started At</th>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '180px' }}>Last Activity</th>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '100px' }}>Duration</th>
                  <th className={styles.tableHeaderCell} style={{ minWidth: '200px' }}>User Email</th>
                </tr>
              </thead>
              <tbody>
                {paginatedSessions.map((session, index) => (
                  <tr key={session.session_id} className={styles.tableRow}>
                    <td className={styles.tableCell}>
                      <span 
                        className={styles.truncate} 
                        title={session.session_id}
                        style={{ maxWidth: '180px' }}
                      >
                        {session.session_id}
                      </span>
                    </td>
                    
                    <td className={styles.tableCell}>
                      {session.user_id ? (
                        <span 
                          className={styles.truncate}
                          title={session.user_id}
                          style={{ maxWidth: '130px' }}
                        >
                          {session.user_id}
                        </span>
                      ) : (
                        <span style={{ color: '#999', fontSize: '12px' }}>Anonymous</span>
                      )}
                    </td>
                    
                    <td className={styles.tableCell}>
                      {getStatusChip(session.status)}
                    </td>
                    
                    <td className={styles.tableCell}>
                      <span className={`${styles.chip} ${styles.chipPrimary}`}>
                        {session.current_step_code}. {session.current_step}
                      </span>
                    </td>
                    
                    <td className={styles.tableCell}>
                      <strong style={{ color: '#667eea' }}>
                        {session.steps_completed} / 6
                      </strong>
                    </td>
                    
                    <td className={styles.tableCell} style={{ fontSize: '13px' }}>
                      {formatDateTime(session.started_at)}
                    </td>
                    
                    <td className={styles.tableCell} style={{ fontSize: '13px' }}>
                      {formatDateTime(session.last_activity)}
                    </td>
                    
                    <td className={styles.tableCell}>
                      <strong style={{ color: '#667eea' }}>
                        {formatDuration(session.duration_seconds)}
                      </strong>
                    </td>
                    
                    <td className={styles.tableCell} style={{ fontSize: '13px' }}>
                      {session.user_email || 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {/* Pagination */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '16px 24px',
            borderTop: '1px solid #e0e0e0',
            background: '#f8f9fa'
          }}>
            <div style={{ color: '#666', fontSize: '14px' }}>
              Page {page + 1} of {totalPages} • 
              Showing {page * rowsPerPage + 1}-{Math.min((page + 1) * rowsPerPage, filteredSessions.length)} of {filteredSessions.length}
            </div>
            
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
              <label style={{ fontSize: '14px', color: '#666' }}>
                Rows per page:
                <select
                  value={rowsPerPage}
                  onChange={handleChangeRowsPerPage}
                  style={{
                    marginLeft: '8px',
                    padding: '4px 8px',
                    border: '1px solid #e0e0e0',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  <option value={10}>10</option>
                  <option value={25}>25</option>
                  <option value={50}>50</option>
                  <option value={100}>100</option>
                </select>
              </label>
              
              <button
                onClick={() => handleChangePage(page - 1)}
                disabled={page === 0}
                style={{
                  padding: '8px 16px',
                  background: page === 0 ? '#e0e0e0' : 'linear-gradient(135deg, #667eea, #764ba2)',
                  color: page === 0 ? '#999' : 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: page === 0 ? 'not-allowed' : 'pointer',
                  fontWeight: 600
                }}
              >
                ← Previous
              </button>
              
              <button
                onClick={() => handleChangePage(page + 1)}
                disabled={page >= totalPages - 1}
                style={{
                  padding: '8px 16px',
                  background: page >= totalPages - 1 ? '#e0e0e0' : 'linear-gradient(135deg, #667eea, #764ba2)',
                  color: page >= totalPages - 1 ? '#999' : 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: page >= totalPages - 1 ? 'not-allowed' : 'pointer',
                  fontWeight: 600
                }}
              >
                Next →
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className={styles.emptyState}>
          <div style={{ fontSize: '80px', marginBottom: '24px' }}>📊</div>
          <h2 className={styles.emptyStateTitle}>No Sessions Found</h2>
          <p className={styles.emptyStateText}>
            {searchTerm || statusFilter !== 'all' || stepFilter !== 'all' 
              ? 'Try adjusting your filters to see more results'
              : 'No registration sessions have been recorded yet'}
          </p>
          {(searchTerm || statusFilter !== 'all' || stepFilter !== 'all') && (
            <button
              className={styles.searchButton}
              onClick={clearFilters}
              style={{ marginTop: '24px' }}
            >
              Clear All Filters
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default AnalyticsLogsPage;