# src/govagent/guards/semantic.py
import logging
import numpy as np
from typing import List

logger = logging.getLogger("govagent.guards.semantic")

class SemanticGuard:
    """
    Qualitative Integrity Layer (v3.0.0).
    Uses localized Sentence-Transformer embeddings to evaluate prompt intent
    and agent reasoning chains against corporate compliance boundaries.
    """
    def __init__(self, mission: str, prohibited: List[str], threshold: float = 0.60):
        self.mission = mission
        self.prohibited = prohibited
        self.threshold = threshold
        
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("🧠 SemanticGuard: Initializing localized SentenceTransformer embedding engine...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            if self.prohibited:
                # Pre-calculate and normalize embedding vectors immediately to save overhead
                embeddings = self.model.encode(self.prohibited, convert_to_numpy=True)
                norms = np.linalg.norm(embeddings, axis=-1, keepdims=True)
                self.prohibited_embeddings = embeddings / (norms + 1e-8)
            else:
                self.prohibited_embeddings = np.empty((0, 384))
        except ImportError:
            logger.critical("🛑 GOVERNANCE CRASH: 'sentence-transformers' package not found in active poetry environment.")
            raise ImportError(
                "Framework initialization failed: Ensure you run `poetry add sentence-transformers` "
                "to activate the v3.0.0 qualitative vector perimeters."
            )

    def _calculate_max_similarity(self, target_vector: np.ndarray) -> float:
        """Computes accurate cosine similarity vectors against normalized prohibited bounds."""
        target_norm = np.linalg.norm(target_vector)
        if target_norm < 1e-8:
            return 0.0
        
        # Normalize the incoming target vector
        normalized_target = target_vector / target_norm
        
        # Calculate dot product against pre-normalized array shapes
        similarities = np.dot(self.prohibited_embeddings, normalized_target)
        return float(np.max(similarities))

    def evaluate_alignment(self, agent_thought: str) -> float:
        """
        Calculates maximum cosine similarity against prohibited corporate strategies.
        Returns 0.0 on a strict circuit breaker breach, or the proximity margin.
        """
        if not agent_thought.strip() or self.prohibited_embeddings.shape[0] == 0:
            return 1.0

        # Encode current agent reasoning signature locally
        target_vector = self.model.encode(agent_thought, convert_to_numpy=True)
        
        # Perform explicit matrix sweep
        max_violation_score = self._calculate_max_similarity(target_vector)
        
        logger.info(f"🧠 SemanticGuard: Vector comparison sweep hit a maximum proximity index of {max_violation_score:.4f}")
        
        # Direct circuit trip if proximity breaches the defined tolerance threshold
        if max_violation_score >= self.threshold:
            logger.warning(f"🛑 [govAgent Semantic Breach] Prohibited intent matching threshold hit: Max Sim {max_violation_score:.4f} >= Tolerance {self.threshold}")
            return 0.0
            
        return float(1.0 - max_violation_score)