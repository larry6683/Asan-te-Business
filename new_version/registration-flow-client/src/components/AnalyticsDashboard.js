import React, { useState, useEffect } from "react";
import styles from "./AnalyticsDashboard.module.css";
import { analyticsService } from "../api/analyticsService";

const AnalyticsDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const [sessions, setSessions] = useState([]);
  
  // Pagination settings
  const [page, setPage] = useState(0);
  const [rowsPerPage] = useState(25);
  
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  // ✅ NEW: Reset pagination when filters change
  useEffect(() => {
    setPage(0);
  }, [statusFilter, typeFilter, searchTerm]);

  const loadAnalyticsData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [statsData] = await Promise.all([
        analyticsService.getRegistrationStats(),
      ]);
      setStats(statsData);
      await loadSessionsData();
    } catch (err) {
      console.error('Error loading analytics:', err);
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
        setSessions([]);
    }
  };

  // --- Formatters ---
  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return '-';
    return new Date(dateTimeString).toLocaleString('en-US', {
      month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
    });
  };

  const formatDuration = (seconds) => {
    if (!seconds || seconds < 0) return '-';
    const m = Math.floor(seconds / 60);
    const s = Math.round(seconds % 60);
    return m < 60 ? `${m}m ${s}s` : `${Math.floor(m/60)}h ${m%60}m`;
  };

  const getStatusChip = (session) => {
    if (session.appUserId) {
      return <span className={`${styles.chip} ${styles.chipSuccess}`}>Complete</span>;
    }
    return <span className={`${styles.chip} ${styles.chipWarning}`}>Incomplete</span>;
  };

  // --- Filtering ---
  const getFilteredSessions = () => {
    let filtered = [...sessions];
    if (statusFilter !== 'all') filtered = filtered.filter(s => s.status === statusFilter);
    if (typeFilter !== 'all') filtered = filtered.filter(s => s.userType === typeFilter);
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

  const filteredSessions = getFilteredSessions();
  const totalPages = Math.ceil(filteredSessions.length / rowsPerPage);
  const paginatedSessions = filteredSessions.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  if (loading) return <div className={styles.container}>Loading...</div>;

  return (
    <div className={styles.container}>
      {/* Header */}
      <div className={styles.header}>
        <h1 className={styles.title}>📊 Registration Logs</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className={styles.refreshButton} onClick={loadAnalyticsData} title="Refresh">↻</button>
        </div>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Total Sessions</div>
            <div className={styles.statValue}>{stats.totalSessions || 0}</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Total Users</div>
            <div className={styles.statValue} style={{ color: '#6366f1' }}>{stats.totalUsers || 0}</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Businesses</div>
            <div className={styles.statValue} style={{ color: '#10b981' }}>{stats.totalBusinesses || 0}</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statLabel}>Non-Profits</div>
            <div className={styles.statValue} style={{ color: '#f59e0b' }}>{stats.totalNonProfits || 0}</div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className={styles.searchSection}>
        <div className={styles.searchGrid}>
          <input
            className={styles.searchInput}
            placeholder="Search ID, Email, Name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <select className={styles.filterSelect} value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="all">All Statuses</option>
            <option value="Completed">Completed</option>
            <option value="In Progress">In Progress</option>
          </select>
          <select className={styles.filterSelect} value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
             <option value="all">All Types</option>
             <option value="Business">Business</option>
             <option value="Non-Profit">Non-Profit</option>
             <option value="Guest">Guest</option>
          </select>
          <button className={styles.searchButton} onClick={() => {setSearchTerm(''); setStatusFilter('all'); setTypeFilter('all');}}>Clear</button>
        </div>
      </div>

      {/* Table Section */}
      <div className={styles.tableContainer}>
        <div className={styles.tableScrollArea}>
          <table className={styles.table}>
            <thead className={styles.tableHead}>
              <tr>
                {/* ✅ NEW: S.No Column Header */}
                <th className={styles.tableHeaderCell} style={{ width: '60px' }}>S.No</th>
                <th className={styles.tableHeaderCell}>Session ID</th>
                <th className={styles.tableHeaderCell}>User ID</th>
                <th className={styles.tableHeaderCell}>Email</th>
                <th className={styles.tableHeaderCell}>Type</th>
                <th className={styles.tableHeaderCell}>Name</th>
                <th className={styles.tableHeaderCell}>Size</th>
                <th className={styles.tableHeaderCell}>State</th>
                <th className={styles.tableHeaderCell}>Website</th>
                <th className={styles.tableHeaderCell}>Status</th>
                <th className={styles.tableHeaderCell}>Started</th>
                <th className={styles.tableHeaderCell}>Duration</th>
              </tr>
            </thead>
            <tbody>
              {paginatedSessions.map((session, index) => (
                <tr key={session.sessionId} className={styles.tableRow}>
                  {/* ✅ NEW: S.No Calculation */}
                  <td className={styles.tableCell}>
                    <strong>{(page * rowsPerPage) + index + 1}</strong>
                  </td>
                  <td className={styles.tableCell}>
                    <span className={styles.truncate} title={session.sessionId}>{session.sessionId}</span>
                  </td>
                  <td className={styles.tableCell}>
                    <span className={styles.truncate} title={session.appUserId}>{session.appUserId || 'Anonymous'}</span>
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
                    {session.website ? <a href={session.website.startsWith('http') ? session.website : `https://${session.website}`} target="_blank" rel="noreferrer">Link</a> : '-'}
                  </td>
                  <td className={styles.tableCell}>{getStatusChip(session)}</td>
                  <td className={styles.tableCell}>{formatDateTime(session.startedAt)}</td>
                  <td className={styles.tableCell}>{formatDuration(session.durationSeconds)}</td>
                </tr>
              ))}
              {paginatedSessions.length === 0 && (
                <tr>
                  <td colSpan="12" style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
                    No records found matching your criteria.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        
        {/* Pagination Footer */}
        <div className={styles.pagination}>
             <button disabled={page===0} onClick={() => setPage(page-1)}>Previous</button>
             <span>Page {page+1} of {totalPages || 1}</span>
             <button disabled={page>=totalPages-1} onClick={() => setPage(page+1)}>Next</button>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;