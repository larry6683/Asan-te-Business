import React, { useState, useEffect } from "react";
import styles from "./AnalyticsDashboard.module.css";
import { analyticsService } from "../api/analyticsService";

const AnalyticsPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const [sessions, setSessions] = useState([]);
  
  // Pagination
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  
  // Filters
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all'); // New filter for User Type
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  const loadAnalyticsData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('📊 Loading analytics logs...');
      
      const [statsData] = await Promise.all([
        analyticsService.getRegistrationStats(),
      ]);

      setStats(statsData);
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
        const sessionsData = await analyticsService.getAllSessions();
        setSessions(sessionsData);
    } catch (err) {
        console.error('Error loading sessions:', err);
        setSessions([]);
    }
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


  // UPDATED: Status logic based on User ID presence
 const getStatusChip = (session) => {
    if (session.appUserId) {
      return (
        <span className={`${styles.chip} ${styles.chipSuccess}`}>
          ✓ Complete
        </span>
      );
    }
    
    return (
      <span className={`${styles.chip} ${styles.chipWarning}`}>
        ⚠ Incomplete
      </span>
    );
  };

  const exportToCSV = () => {
    const headers = [
      'Session ID', 'User ID', 'User Email', 'User Type', 
      'Name', 'Size', 'State', 'Website', 'Categories',
      'Status', 'Started At', 'Last Activity', 'Duration'
    ];
    
    let csvContent = headers.join(',') + '\n';
    
    const filteredSessions = getFilteredSessions();
    filteredSessions.forEach(s => {
      const row = [
        `"${s.sessionId}"`, s.appUserId || 'Anonymous', s.userEmail || 'N/A', s.userType || 'Guest',
        `"${s.entityName}"`, `"${s.entitySize}"`, s.entityState, `"${s.website}"`, `"${(s.categories || []).join('; ')}"`,
        s.status, `"${s.startedAt}"`, `"${s.lastActivity}"`, s.durationSeconds
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
    
    if (typeFilter !== 'all') {
       filtered = filtered.filter(s => s.userType === typeFilter);
    }
    
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(s => 
        s.sessionId.toLowerCase().includes(term) ||
        s.appUserId?.toLowerCase().includes(term) ||
        s.userEmail?.toLowerCase().includes(term) ||
        s.entityName?.toLowerCase().includes(term)
      );
    }
    
    return filtered;
  };

  const paginatedSessions = getFilteredSessions().slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  if (loading) return <div className={styles.container}>Loading...</div>;

  const filteredSessions = getFilteredSessions();
  const totalPages = Math.ceil(filteredSessions.length / rowsPerPage);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>📊 Registration Logs</h1>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className={styles.refreshButton} onClick={exportToCSV} title="Export CSV">💾</button>
          <button className={styles.refreshButton} onClick={loadAnalyticsData} title="Refresh">🔄</button>
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
          {/* Card 1: Total Sessions */}
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Real-Time Unique Sessions</div>
            <div className={styles.statValue}>{stats.totalSessions || 0}</div>
          </div>
          
          {/* Card 2: Total Users */}
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Total Users</div>
            <div className={styles.statValue} style={{ color: '#667eea' }}>
              {stats.totalUsers || 0}
            </div>
          </div>
          
          {/* Card 3: Total Businesses */}
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Registered Businesses</div>
            <div className={styles.statValue} style={{ color: '#2e7d32' }}>
              {stats.totalBusinesses || 0}
            </div>
          </div>
          
          {/* Card 4: Total Non-Profits */}
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Registered Non-Profits</div>
            <div className={styles.statValue} style={{ color: '#e65100' }}>
              {stats.totalNonProfits || 0}
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className={styles.searchSection}>
        <div className={styles.searchGrid}>
          <input
            type="text"
            className={styles.searchInput}
            placeholder="Search ID, Email, Name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className={styles.filterSelect}>
            <option value="all">All Statuses</option>
            <option value="Completed">Completed</option>
            <option value="In Progress">In Progress</option>
            <option value="Abandoned">Abandoned</option>
          </select>
          <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)} className={styles.filterSelect}>
             <option value="all">All Types</option>
             <option value="Business">Business</option>
             <option value="Non-Profit">Non-Profit</option>
             <option value="Guest">Guest/Anonymous</option>
          </select>
          <button className={styles.searchButton} onClick={() => {setSearchTerm(''); setStatusFilter('all'); setTypeFilter('all');}}>Clear</button>
        </div>
        <div style={{marginTop: '10px', color: '#666'}}>Showing {filteredSessions.length} sessions</div>
      </div>

      {/* Table */}
      <div className={styles.tableContainer}>
        <div style={{ overflowX: 'auto' }}>
          <table className={styles.table} style={{ minWidth: '1600px' }}>
            <thead className={styles.tableHead}>
              <tr>
                <th className={styles.tableHeaderCell}>Session ID</th>
                <th className={styles.tableHeaderCell}>User ID</th>
                <th className={styles.tableHeaderCell}>Email</th>
                <th className={styles.tableHeaderCell}>Type</th>
                <th className={styles.tableHeaderCell}>Name</th>
                <th className={styles.tableHeaderCell}>Size</th>
                <th className={styles.tableHeaderCell}>State</th>
                <th className={styles.tableHeaderCell}>Website</th>
                <th className={styles.tableHeaderCell} style={{maxWidth: '200px'}}>Categories</th>
                <th className={styles.tableHeaderCell}>Status</th>
                <th className={styles.tableHeaderCell}>Started</th>
                <th className={styles.tableHeaderCell}>Last Active</th>
                <th className={styles.tableHeaderCell}>Duration</th>
              </tr>
            </thead>
            <tbody>
              {paginatedSessions.map((session) => (
                <tr key={session.sessionId} className={styles.tableRow}>
                  <td className={styles.tableCell} title={session.sessionId}>
                    <span className={styles.truncate} style={{maxWidth: '100px'}}>{session.sessionId}</span>
                  </td>
                  <td className={styles.tableCell} title={session.appUserId}>
                    <span className={styles.truncate} style={{maxWidth: '100px'}}>{session.appUserId || 'Anonymous'}</span>
                  </td>
                  <td className={styles.tableCell}>{session.userEmail || '-'}</td>
                  <td className={styles.tableCell}>
                    <span className={`${styles.chip} ${session.userType === 'Business' ? styles.chipPrimary : session.userType === 'Non-Profit' ? styles.chipSuccess : ''}`}>
                        {session.userType || 'Guest'}
                    </span>
                  </td>
                  <td className={styles.tableCell}>{session.entityName || '-'}</td>
                  <td className={styles.tableCell}>{session.entitySize || '-'}</td>
                  <td className={styles.tableCell}>{session.entityState || '-'}</td>
               <td className={styles.tableCell}>
  {session.website && session.website !== '-' ? (
    <a 
      href={session.website.startsWith('http') ? session.website : `https://${session.website}`} 
      target="_blank" 
      rel="noreferrer"
    >
      Link
    </a>
  ) : '-'}
</td>
                  <td className={styles.tableCell}>
                    <div className={styles.truncate} style={{maxWidth: '200px'}} title={(session.categories || []).join(', ')}>
                        {(session.categories || []).join(', ')}
                    </div>
                  </td>
                  <td className={styles.tableCell}>{getStatusChip(session)}</td>
                  <td className={styles.tableCell} style={{ fontSize: '12px' }}>{formatDateTime(session.startedAt)}</td>
                  <td className={styles.tableCell} style={{ fontSize: '12px' }}>{formatDateTime(session.lastActivity)}</td>
                  <td className={styles.tableCell}><strong>{formatDuration(session.durationSeconds)}</strong></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {/* Pagination Controls (reuse existing logic) */}
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '16px' }}>
             <button disabled={page===0} onClick={() => setPage(page-1)}>Previous</button>
             <span>Page {page+1} of {totalPages}</span>
             <button disabled={page>=totalPages-1} onClick={() => setPage(page+1)}>Next</button>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;