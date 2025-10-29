
# vector_services.py - UPDATED FOR HACKATHON READINESS
import mariadb
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class GreenJobsVectorService:
    def __init__(self):
        # Initialize the embedding model (384 dimensions)
        print("🔄 Loading sentence transformer model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded successfully!")
        
        # Database connection using your existing config
        try:
            self.conn = mariadb.connect(
                host='localhost',
                user='root', 
                password='Shivam@12345',
                database='green_jobs',
                port=3306
            )
            print("✅ Database connection established!")
        except mariadb.Error as e:
            print(f"❌ Error connecting to MariaDB: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """Convert text to vector embedding using 384 dimensions"""
        if not text or text.strip() == "":
            return [0.0] * 384
        return self.model.encode(text).tolist()
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            v1 = np.array(vec1)
            v2 = np.array(vec2)
            dot_product = np.dot(v1, v2)
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            
            if norm_v1 == 0 or norm_v2 == 0:
                return 0.0
            return dot_product / (norm_v1 * norm_v2)
        except Exception as e:
            print(f"❌ Cosine similarity error: {e}")
            return 0.0

    def populate_existing_data(self):
        """HACKATHON READY: Add vector embeddings to all existing data"""
        cursor = self.conn.cursor()
        
        print("🚀 Starting vector data population for hackathon...")
        
        # Ensure vector columns exist
        try:
            cursor.execute("ALTER TABLE careers ADD COLUMN IF NOT EXISTS desc_vector_json TEXT")
            cursor.execute("ALTER TABLE careers ADD COLUMN IF NOT EXISTS skills_vector_json TEXT")
            print("✅ Career vector columns ready")
        except:
            print("✅ Career vector columns already exist")
        
        try:
            cursor.execute("ALTER TABLE jobs ADD COLUMN IF NOT EXISTS desc_vector_json TEXT")
            cursor.execute("ALTER TABLE jobs ADD COLUMN IF NOT EXISTS skills_vector_json TEXT") 
            print("✅ Job vector columns ready")
        except:
            print("✅ Job vector columns already exist")
        
        # Populate careers vectors
        print("📊 Vectorizing careers...")
        cursor.execute("SELECT career_id, title, description, required_skills FROM careers")
        careers = cursor.fetchall()
        
        success_count = 0
        for career_id, title, description, skills in careers:
            try:
                # Generate embeddings
                desc_text = f"{title} {description}" if description else title
                desc_vector = self.generate_embedding(desc_text)
                
                skills_text = str(skills) if skills else title
                skills_vector = self.generate_embedding(skills_text)
                
                # Store as JSON
                desc_vector_json = json.dumps(desc_vector)
                skills_vector_json = json.dumps(skills_vector)
                
                cursor.execute("""
                    UPDATE careers 
                    SET desc_vector_json = ?, skills_vector_json = ?
                    WHERE career_id = ?
                """, (desc_vector_json, skills_vector_json, career_id))
                
                success_count += 1
                if success_count % 10 == 0:
                    print(f"✅ Vectorized {success_count} careers...")
                    
            except Exception as e:
                print(f"⚠️ Skipping career {career_id}: {e}")
                continue
        
        # Populate jobs vectors
        print("💼 Vectorizing jobs...")
        cursor.execute("SELECT job_id, title, description, company FROM jobs")
        jobs = cursor.fetchall()
        
        job_count = 0
        for job_id, title, description, company in jobs:
            try:
                desc_text = f"{title} {description} {company}" if description else f"{title} {company}"
                desc_vector = self.generate_embedding(desc_text)
                
                skills_vector = self.generate_embedding(description if description else title)
                
                desc_vector_json = json.dumps(desc_vector)
                skills_vector_json = json.dumps(skills_vector)
                
                cursor.execute("""
                    UPDATE jobs 
                    SET desc_vector_json = ?, skills_vector_json = ?
                    WHERE job_id = ?
                """, (desc_vector_json, skills_vector_json, job_id))
                
                job_count += 1
                if job_count % 10 == 0:
                    print(f"✅ Vectorized {job_count} jobs...")
                    
            except Exception as e:
                print(f"⚠️ Skipping job {job_id}: {e}")
                continue
        
        self.conn.commit()
        print(f"🎉 HACKATHON READY: {success_count} careers + {job_count} jobs vectorized!")
        return True

    # HACKATHON-READY SEMANTIC SEARCH
    def semantic_search_jobs(self, query: str, top_k: int = 10, filters: Dict = None) -> List[Dict]:
        """HACKATHON ENDPOINT: Semantic job search"""
        query_vector = self.generate_embedding(query)
        
        cursor = self.conn.cursor(dictionary=True)
        
        # Get all active jobs
        base_query = """
            SELECT job_id, title, description, company, location, salary,
                   desc_vector_json, skills_vector_json
            FROM jobs 
            WHERE 1=1
        """
        params = []
        
        if filters:
            if filters.get('location'):
                base_query += " AND location LIKE ?"
                params.append(f"%{filters['location']}%")
        
        cursor.execute(base_query, params)
        all_jobs = cursor.fetchall()
        
        # Calculate similarities
        scored_jobs = []
        for job in all_jobs:
            if job['desc_vector_json']:
                try:
                    job_vector = json.loads(job['desc_vector_json'])
                    similarity = self.cosine_similarity(query_vector, job_vector)
                    
                    if similarity > 0.3:  # Relevance threshold
                        scored_jobs.append({
                            "id": job["job_id"],
                            "title": job["title"],
                            "company": job["company"],
                            "location": job["location"],
                            "salary": f"₹{job['salary']:.1f} LPA" if job['salary'] else "Competitive",
                            "description": job["description"][:150] + "..." if job["description"] and len(job["description"]) > 150 else job["description"],
                            "similarity_score": round(similarity * 100, 2),
                            "search_tech": "AI Semantic Search",
                            "status": "Hackathon Ready 🚀"
                        })
                except Exception as e:
                    continue
        
        scored_jobs.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_jobs[:top_k]

    def semantic_career_recommendations(self, query: str, top_k: int = 10) -> List[Dict]:
        """HACKATHON ENDPOINT: AI career recommendations"""
        query_vector = self.generate_embedding(query)
        
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT career_id, title, description, growth, salary_range, demand, category,
                   skills_vector_json
            FROM careers 
        """)
        
        all_careers = cursor.fetchall()
        
        recommendations = []
        for career in all_careers:
            if career['skills_vector_json']:
                try:
                    career_vector = json.loads(career['skills_vector_json'])
                    similarity = self.cosine_similarity(query_vector, career_vector)
                    
                    recommendations.append({
                        "id": career["career_id"],
                        "title": career["title"],
                        "description": career["description"],
                        "growth": career["growth"],
                        "salary_range": career["salary_range"],
                        "demand": career["demand"],
                        "category": career["category"],
                        "similarity_score": round(similarity * 100, 2),
                        "ai_tech": "Vector Similarity",
                        "status": "AI Recommended 🎯"
                    })
                except Exception as e:
                    continue
        
        recommendations.sort(key=lambda x: x["similarity_score"], reverse=True)
        return recommendations[:top_k]

    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Global instance
vector_service = GreenJobsVectorService()

def initialize_vector_data():
    """Initialize vector data for hackathon"""
    try:
        success = vector_service.populate_existing_data()
        return {"status": "success" if success else "failed", "message": "Vector data populated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def test_vector_functionality():
    """Test vector functionality for hackathon demo"""
    try:
        print("🧪 Testing hackathon vector endpoints...")
        
        # Test job search
        jobs = vector_service.semantic_search_jobs("solar energy engineer", top_k=2)
        print("✅ Semantic job search working!")
        
        # Test career recommendations
        careers = vector_service.semantic_career_recommendations("python data analysis", top_k=2)
        print("✅ Career recommendations working!")
        
        return {
            "status": "success",
            "message": "All vector endpoints ready for hackathon!",
            "test_results": {
                "job_search": len(jobs),
                "career_recommendations": len(careers)
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Run this file directly to test the vector functionality
    result = test_vector_functionality()
    print(result)



