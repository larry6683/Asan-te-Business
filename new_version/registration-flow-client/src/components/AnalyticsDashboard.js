import React, { useState, useEffect, useRef } from "react";
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

  // --- Snapshot & Automation State ---
  const [showSnapshotModal, setShowSnapshotModal] = useState(false);
  const [isAutoActive, setIsAutoActive] = useState(false);
  const [snapshotConfig, setSnapshotConfig] = useState({
    fileName: 'analytics_report',
    frequency: 1, // minutes
    mode: 'full' // 'full' or 'incremental'
  });
  const [lastSnapshotTime, setLastSnapshotTime] = useState(null);
  const autoTimerRef = useRef(null);

  useEffect(() => {
    loadAnalyticsData();
  }, []);

  // Reset pagination when filters change
  useEffect(() => {
    setPage(0);
  }, [statusFilter, typeFilter, searchTerm]);

  // --- Automation Effect ---
  useEffect(() => {
    if (isAutoActive) {
      const intervalMs = snapshotConfig.frequency * 60 * 1000;
      
      // Initial run logic or wait for first interval? 
      // Usually wait for interval.
      autoTimerRef.current = setInterval(() => {
        performAutoSnapshot();
      }, intervalMs);
    } else {
      if (autoTimerRef.current) clearInterval(autoTimerRef.current);
    }

    return () => {
      if (autoTimerRef.current) clearInterval(autoTimerRef.current);
    };
  }, [isAutoActive, snapshotConfig, sessions]); // Re-bind if sessions/config update

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

  // --- CSV Generation & Download Logic ---
  const convertToCSV = (data) => {
    const headers = [
      "Session ID", "User ID", "Email", "Type", 
      "Entity Name", "Size", "State", "Website", 
      "Status", "Started At", "Last Activity", "Duration (s)"
    ];

    const rows = data.map(s => [
      s.sessionId,
      s.appUserId || 'Anonymous',
      s.userEmail || '-',
      s.userType || 'Guest',
      `"${s.entityName || '-'}"`, // Quote to handle commas in names
      s.entitySize || '-',
      s.entityState || '-',
      s.website || '-',
      s.appUserId ? 'Complete' : 'Incomplete',
      s.startedAt,
      s.lastActivity,
      s.durationSeconds
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(r => r.join(','))
    ].join('\n');

    return csvContent;
  };

  const triggerDownload = (csvData, filename) => {
    const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('button'); // using generic element logic
    const url = URL.createObjectURL(blob);
    
    const downloadLink = document.createElement("a");
    downloadLink.href = url;
    downloadLink.setAttribute("download", `${filename}.csv`);
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  };

  const handleManualSnapshot = () => {
    const filtered = getFilteredSessions(); // Respect current filters
    const csv = convertToCSV(filtered);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    triggerDownload(csv, `Analytics_Snapshot_${timestamp}`);
  };

  const performAutoSnapshot = () => {
    // Refresh data first to ensure we have latest
    loadSessionsData().then(() => {
        // We must use functional state or a ref for 'sessions' if inside closure, 
        // but here we rely on the useEffect dependency re-binding.
        
        let dataToExport = [...sessions];
        
        // Apply "Append" logic (Incremental)
        if (snapshotConfig.mode === 'incremental' && lastSnapshotTime) {
            dataToExport = dataToExport.filter(s => new Date(s.startedAt) > lastSnapshotTime);
        }

        if (dataToExport.length === 0 && snapshotConfig.mode === 'incremental') {
            console.log("Auto-Snapshot: No new data found.");
            return;
        }

        const csv = convertToCSV(dataToExport);
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        // Simulate "New Folder" by using a prefix that groups them when sorted
        const folderPrefix = "AutoSnapshot_"; 
        const filename = `${folderPrefix}${snapshotConfig.fileName}_${timestamp}`;
        
        triggerDownload(csv, filename);
        setLastSnapshotTime(new Date());
        console.log(`Auto-Snapshot triggered: ${filename}`);
    });
  };

  const toggleAutoSnapshot = () => {
    if (isAutoActive) {
        setIsAutoActive(false);
    } else {
        setLastSnapshotTime(new Date()); // Set start time marks
        setIsAutoActive(true);
        setShowSnapshotModal(false);
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
    
    if (statusFilter !== 'all') {
        if (statusFilter === 'Complete') {
            filtered = filtered.filter(s => s.appUserId);
        } else if (statusFilter === 'Incomplete') {
            filtered = filtered.filter(s => !s.appUserId);
        }
    }

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
        <div style={{ display: 'flex', gap: '12px' }}>
          
          {/* Snapshot Controls */}
          <button 
            className={`${styles.actionButton} ${styles.primaryBtn}`} 
            onClick={handleManualSnapshot}
            title="Download CSV of current view"
          >
            📥 Snapshot CSV
          </button>
          
          <button 
            className={`${styles.actionButton} ${isAutoActive ? styles.activeBtn : styles.secondaryBtn}`} 
            onClick={() => setShowSnapshotModal(true)}
            title="Configure automated snapshots"
          >
            {isAutoActive ? '⚙️ Auto: ON' : '⚙️ Auto Snapshot'}
          </button>

          <button className={styles.refreshButton} onClick={loadAnalyticsData} title="Refresh Data">↻</button>
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
            <option value="Complete">Complete</option>
            <option value="Incomplete">Incomplete</option>
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

      {/* Result Count */}
      <div className={styles.resultCount}>
            Showing <strong className={styles.showingNumberofRows}>{filteredSessions.length}</strong> sessions out of <strong>{sessions.length}</strong>
      </div>

      {/* Table Section */}
      <div className={styles.tableContainer}>
        <div className={styles.tableScrollArea}>
          <table className={styles.table}>
            <thead className={styles.tableHead}>
              <tr>
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
        
        <div className={styles.pagination}>
             <button disabled={page===0} onClick={() => setPage(page-1)}>Previous</button>
             <span>Page {page+1} of {totalPages || 1}</span>
             <button disabled={page>=totalPages-1} onClick={() => setPage(page+1)}>Next</button>
        </div>
      </div>

      {/* --- Configuration Modal --- */}
      {showSnapshotModal && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <div className={styles.modalHeader}>
              <h3>⚙️ Configure Auto-Snapshot</h3>
              <button className={styles.closeBtn} onClick={() => setShowSnapshotModal(false)}>×</button>
            </div>
            
            <div className={styles.modalBody}>
              <div className={styles.formGroup}>
                <label>Base File Name</label>
                <input 
                  type="text" 
                  value={snapshotConfig.fileName} 
                  onChange={(e) => setSnapshotConfig({...snapshotConfig, fileName: e.target.value})}
                />
              </div>
              
              <div className={styles.formGroup}>
                <label>Frequency (Minutes)</label>
                <input 
                  type="number" 
                  min="1" 
                  value={snapshotConfig.frequency} 
                  onChange={(e) => setSnapshotConfig({...snapshotConfig, frequency: parseInt(e.target.value) || 1})}
                />
              </div>

              <div className={styles.formGroup}>
                <label>Export Mode</label>
                <div className={styles.radioGroup}>
                    <label>
                        <input 
                            type="radio" 
                            checked={snapshotConfig.mode === 'full'} 
                            onChange={() => setSnapshotConfig({...snapshotConfig, mode: 'full'})}
                        />
                        Full Snapshot (Overwrite)
                    </label>
                    <label>
                        <input 
                            type="radio" 
                            checked={snapshotConfig.mode === 'incremental'} 
                            onChange={() => setSnapshotConfig({...snapshotConfig, mode: 'incremental'})}
                        />
                        Incremental (New data only - "Append")
                    </label>
                </div>
                <p className={styles.hint}>
                    * Incremental mode will download a new CSV containing only rows created since the last snapshot.
                </p>
              </div>
            </div>

            <div className={styles.modalFooter}>
              <button className={styles.secondaryBtn} onClick={() => setShowSnapshotModal(false)}>Cancel</button>
              
              {isAutoActive ? (
                <button className={`${styles.actionButton} ${styles.dangerBtn}`} onClick={toggleAutoSnapshot}>
                    Stop Automation
                </button>
              ) : (
                <button className={`${styles.actionButton} ${styles.primaryBtn}`} onClick={toggleAutoSnapshot}>
                    Start Automation
                </button>
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default AnalyticsDashboard;