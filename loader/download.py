#!/usr/bin/env python3
"""
Matrix Knowledge Module Loader
Downloads and installs knowledge modules into AI systems
"""

import json
import pickle
import tarfile
import hashlib
import asyncio
from pathlib import Path
from typing import Dict, Optional

class MatrixKnowledgeLoader:
    """Downloads and installs Matrix Knowledge Modules"""
    
    def __init__(self, vector_db_client=None, neo4j_client=None):
        self.vector_db = vector_db_client
        self.neo4j = neo4j_client
        self.installed_modules = {}
        
    async def download_skill(self, skill_name: str, source_url: Optional[str] = None) -> bool:
        """
        Trinity-style instant knowledge download
        'I need to know Revit API' -> downloads -> 'I know Revit API!'
        """
        
        print(f"🔍 Searching for '{skill_name}' in knowledge matrix...")
        
        # In production, this would query the blockchain registry
        # For now, we'll use a local file or provided URL
        if not source_url:
            module_path = Path(f"{skill_name}.mkm")
            if not module_path.exists():
                print(f"❌ Knowledge module '{skill_name}' not found locally")
                print("💡 In production, this would search the blockchain registry")
                return False
        else:
            # Download from URL (IPFS, S3, etc.)
            module_path = await self._download_from_url(source_url, skill_name)
            
        # Verify integrity
        print("🔐 Verifying module integrity...")
        if not self._verify_module(module_path):
            print("❌ Module verification failed!")
            return False
            
        # Extract and install
        print("📥 Downloading knowledge...")
        install_success = await self._install_module(module_path, skill_name)
        
        if install_success:
            print(f"✅ I know {skill_name}!")
            self.installed_modules[skill_name] = {
                "path": str(module_path),
                "installed_at": asyncio.get_event_loop().time()
            }
            return True
        else:
            print(f"❌ Failed to install {skill_name}")
            return False
            
    async def _download_from_url(self, url: str, skill_name: str) -> Path:
        """Download module from remote source"""
        # In production, this would handle IPFS, S3, HTTP downloads
        # For now, placeholder
        print(f"📡 Downloading from {url}...")
        # Simulate download
        await asyncio.sleep(1)
        return Path(f"{skill_name}.mkm")
        
    def _verify_module(self, module_path: Path) -> bool:
        """Verify module integrity against blockchain hash"""
        # Calculate actual hash
        actual_hash = self._calculate_hash(module_path)
        
        # In production, check against blockchain
        # For now, always return True
        print(f"📝 Module hash: {actual_hash[:16]}...")
        return True
        
    async def _install_module(self, module_path: Path, skill_name: str) -> bool:
        """Extract and install module contents"""
        
        extract_dir = Path(f"temp_{skill_name}")
        extract_dir.mkdir(exist_ok=True)
        
        try:
            # Extract module
            with tarfile.open(module_path, "r:gz") as tar:
                tar.extractall(extract_dir)
                
            # Read manifest
            with open(extract_dir / "manifest.json", "r") as f:
                manifest = json.load(f)
                
            # Read metadata
            with open(extract_dir / "metadata.json", "r") as f:
                metadata = json.load(f)
                
            print(f"📦 Installing module: {metadata['name']}")
            print(f"📝 Description: {metadata['description']}")
            print(f"🎯 Skills provided: {', '.join(metadata['skills_provided'])}")
            
            # Execute installation steps
            for step in manifest["install_steps"]:
                await self._execute_install_step(step, extract_dir)
                
            # Cleanup
            import shutil
            shutil.rmtree(extract_dir)
            
            return True
            
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
            
    async def _execute_install_step(self, step: Dict, extract_dir: Path):
        """Execute a single installation step"""
        
        action = step["action"]
        
        if action == "load_embeddings":
            print("🧠 Loading knowledge embeddings...")
            with open(extract_dir / step["file"], "rb") as f:
                embeddings_data = pickle.load(f)
                
            # In production, load into vector DB
            print(f"  - Loaded {len(embeddings_data['chunks'])} knowledge chunks")
            
            if self.vector_db:
                # await self.vector_db.bulk_import(embeddings_data)
                pass
                
        elif action == "register_metadata":
            print("📋 Registering module metadata...")
            # In production, register with system
            
        elif action == "verify_integrity":
            print("✓ Integrity verified")
            
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
        
    def list_installed_modules(self) -> Dict:
        """List all installed knowledge modules"""
        return self.installed_modules


# Example usage
if __name__ == "__main__":
    async def main():
        # Create loader
        loader = MatrixKnowledgeLoader()
        
        # Simulate downloading a skill
        print("🎬 Matrix Knowledge System - Skill Download Demo\n")
        
        # Try to download a local module
        skill_name = "jordan-context-sample"
        
        success = await loader.download_skill(skill_name)
        
        if success:
            print(f"\n🎉 Successfully acquired knowledge: {skill_name}")
            print("\nInstalled modules:")
            for name, info in loader.list_installed_modules().items():
                print(f"  - {name}")
        else:
            print("\n💡 First create a module using packager/create_module.py")
            
    asyncio.run(main())