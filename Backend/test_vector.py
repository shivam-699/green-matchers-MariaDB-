from vector_services import vector_service, initialize_vector_data

def test_vector_service():
    try:
        print("Testing vector service connection...")
        
        # Test database connection
        conn = vector_service.conn
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM careers")
        count = cursor.fetchone()[0]
        print(f"✅ Connected to database. Found {count} careers.")
        
        # Test embedding generation
        test_text = "renewable energy engineer"
        embedding = vector_service.generate_embedding(test_text)
        print(f"✅ Embedding generated: {len(embedding)} dimensions")
        
        # Test similarity calculation
        text1 = "solar energy"
        text2 = "renewable power" 
        vec1 = vector_service.generate_embedding(text1)
        vec2 = vector_service.generate_embedding(text2)
        similarity = vector_service.cosine_similarity(vec1, vec2)
        print(f"✅ Similarity between '{text1}' and '{text2}': {similarity:.4f}")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Vector service test failed: {e}")
        return False

if __name__ == "__main__":
    test_vector_service()