import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../config/axios';
import { PlusCircle, Search, Trash2 } from 'lucide-react';

interface Note {
  id: string;
  title: string;
  content: string;
  owner_email: string;
}

export const Dashboard = () => {
  const { user } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAdmin, setShowAdmin] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    fetchNotes();
  }, [showAdmin]);

  const fetchNotes = async () => {
    setLoading(true);
    try {
      const endpoint = showAdmin ? '/notes/all' : '/notes/';
      const response = await api.get(endpoint);
      setNotes(response.data.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newContent.trim()) return;

    try {
      await api.post('/notes/', { title: newTitle, content: newContent });
      setNewTitle('');
      setNewContent('');
      setIsAdding(false);
      fetchNotes();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container animate-in">
      <div className="dashboard-header">
        <div>
          <h2>Welcome, {user?.name}</h2>
          <p>Email: {user?.email} | Role: <span className={`badge ${user?.role === 'admin' ? 'badge-admin' : 'badge-user'}`}>{user?.role}</span></p>
        </div>
        {user?.role === 'admin' && (
          <button 
            className={`btn ${!showAdmin ? 'btn-outline' : ''}`} 
            onClick={() => setShowAdmin(!showAdmin)}
          >
            {showAdmin ? 'View My Notes' : 'View All Context'}
          </button>
        )}
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <button className="btn" onClick={() => setIsAdding(!isAdding)}>
          <PlusCircle size={18} /> {isAdding ? 'Cancel' : 'New Note'}
        </button>
      </div>

      {isAdding && (
        <div className="card animate-in" style={{ marginBottom: '2rem' }}>
          <h3>Create a Note</h3>
          <form onSubmit={handleCreateNote} style={{ marginTop: '1rem' }}>
            <div className="form-group">
              <input 
                type="text" className="form-input" placeholder="Note Title" 
                value={newTitle} onChange={e => setNewTitle(e.target.value)} required 
              />
            </div>
            <div className="form-group">
              <textarea 
                className="form-input" placeholder="Write something amazing..." 
                rows={4} value={newContent} onChange={e => setNewContent(e.target.value)} required 
              />
            </div>
            <button type="submit" className="btn"><PlusCircle size={18} /> Save Note</button>
          </form>
        </div>
      )}

      {loading ? (
        <p>Loading notes...</p>
      ) : notes.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <Search size={48} color="var(--text-secondary)" style={{ marginBottom: '1rem' }} />
          <h3>No notes found</h3>
          <p>Create your first note by clicking the button above.</p>
        </div>
      ) : (
        <div className="grid">
          {notes.map(note => (
            <div className="card animate-in" key={note.id}>
              <h3 style={{ marginBottom: '0.5rem' }}>{note.title}</h3>
              <p style={{ marginBottom: '1rem', whiteSpace: 'pre-wrap' }}>{note.content}</p>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
                 <small style={{ color: 'var(--text-secondary)' }}>By: {note.owner_email}</small>
                 {showAdmin && note.owner_email !== user?.email && (
                    <span className="badge badge-admin">User Note</span>
                 )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
