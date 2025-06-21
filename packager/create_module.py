#!/usr/bin/env python3
"""
Matrix Knowledge Module Packager
Converts crawled content or memory into downloadable .mkm files
"""

import json
import pickle
import tarfile
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import asyncio

class KnowledgePackager:
    """Creates Matrix Knowledge Modules from various sources"""
    
    def __init__(self):
        self.module_version = "1.0.0"
        
    async def create_from_memory(self, 
                                entities: List[Dict],
                                module_name: str,
                                description: str) -> Path:
        """Package memory entities into a knowledge module"""
        
        print(f"🎬 Creating knowledge module: {module_name}")
        
        # Create module directory
        module_dir = Path(f"temp_{module_name}")
        module_dir.mkdir(exist_ok=True)
        
        # 1. Create metadata
        metadata = {
            "name": module_name,
            "description": description,
            "version": self.module_version,
            "created": datetime.now().isoformat(),
            "type": "memory_export",
            "entity_count": len(entities),
            "skills_provided": self._extract_skills(entities),
            "prerequisites": [],
            "size_estimate_mb": self._estimate_size(entities)
        }
        
        with open(module_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
        # 2. Process entities into embeddings format
        print("🧠 Processing memory entities...")
        embeddings_data = self._create_embeddings_data(entities)
        
        with open(module_dir / "embeddings.pkl", "wb") as f:
            pickle.dump(embeddings_data, f)
            
        # 3. Create sources manifest
        sources = {
            "memory_entities": [e.get("name", "unknown") for e in entities],
            "export_timestamp": datetime.now().isoformat(),
            "total_observations": sum(len(e.get("observations", [])) for e in entities)
        }
        
        with open(module_dir / "sources.json", "w") as f:
            json.dump(sources, f, indent=2)
            
        # 4. Create installation manifest
        manifest = {
            "install_steps": [
                {"action": "load_embeddings", "file": "embeddings.pkl"},
                {"action": "register_metadata", "file": "metadata.json"},
                {"action": "verify_integrity", "check": "hash"}
            ],
            "requirements": {
                "vector_db": "supabase_or_qdrant",
                "min_memory_mb": 100
            }
        }
        
        with open(module_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
            
        # 5. Create the .mkm archive
        print("📦 Packaging module...")
        mkm_path = Path(f"{module_name}.mkm")
        
        with tarfile.open(mkm_path, "w:gz") as tar:
            for file in module_dir.iterdir():
                tar.add(file, arcname=file.name)
                
        # 6. Calculate hash
        module_hash = self._calculate_hash(mkm_path)
        print(f"✅ Module created: {mkm_path} (hash: {module_hash[:16]}...)")
        
        # Cleanup
        import shutil
        shutil.rmtree(module_dir)
        
        return mkm_path
        
    def _extract_skills(self, entities: List[Dict]) -> List[str]:
        """Extract skills/capabilities from entities"""
        skills = set()
        
        for entity in entities:
            entity_type = entity.get("entityType", "")
            name = entity.get("name", "")
            
            if entity_type == "Active_Project":
                skills.add(f"project_{name.lower().replace(' ', '_')}")
            elif entity_type == "Tool_Reference":
                skills.add(f"tool_{name.lower()}")
            elif entity_type == "System_Protocol":
                skills.add(f"protocol_{name.lower().replace(' ', '_')}")
                
        return list(skills)
        
    def _estimate_size(self, entities: List[Dict]) -> float:
        """Estimate compressed size in MB"""
        total_chars = sum(len(str(e)) for e in entities)
        # Rough estimate: 10:1 compression ratio
        return round(total_chars / (1024 * 1024 * 10), 2)
        
    def _create_embeddings_data(self, entities: List[Dict]) -> Dict:
        """Convert entities to embeddings-ready format"""
        embeddings_data = {
            "chunks": [],
            "metadata": [],
            "entity_map": {}
        }
        
        chunk_id = 0
        for entity in entities:
            entity_name = entity.get("name", "unknown")
            entity_type = entity.get("entityType", "unknown")
            
            # Each observation becomes a chunk
            for obs in entity.get("observations", []):
                embeddings_data["chunks"].append({
                    "id": chunk_id,
                    "text": obs,
                    "entity": entity_name,
                    "type": entity_type
                })
                
                embeddings_data["metadata"].append({
                    "chunk_id": chunk_id,
                    "entity_name": entity_name,
                    "entity_type": entity_type,
                    "char_count": len(obs)
                })
                
                chunk_id += 1
                
            embeddings_data["entity_map"][entity_name] = entity_type
            
        return embeddings_data
        
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


# Example usage
if __name__ == "__main__":
    import sys
    
    async def main():
        packager = KnowledgePackager()
        
        # Example: Package some sample entities
        sample_entities = [
            {
                "name": "Session_Breadcrumbs",
                "entityType": "Activity_Log",
                "observations": [
                    "[2025-06-20][Project started]",
                    "[2025-06-21][Matrix Knowledge System designed]"
                ]
            },
            {
                "name": "Matrix_Knowledge_System",
                "entityType": "Active_Project",
                "observations": [
                    "Trinity-style downloadable knowledge modules",
                    "Integrates with blockchain for verification"
                ]
            }
        ]
        
        module_path = await packager.create_from_memory(
            entities=sample_entities,
            module_name="jordan-context-sample",
            description="Sample Jordan Ehrig project context"
        )
        
        print(f"\n🎉 Knowledge module created: {module_path}")
        print("\nNext steps:")
        print("1. Upload to IPFS/S3")
        print("2. Register on blockchain")
        print("3. Share with other AI agents!")
        
    asyncio.run(main())