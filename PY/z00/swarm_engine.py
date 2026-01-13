import hashlib
import time
from typing import List, Dict, Optional

# Σ-GLYPH: SWARM ENGINE (V1.1 - Retro-Resonance Edition)
# Розраховує перерозподіл енергії (ресурсів) у Рою на основі сили інтенту.
# Впроваджено підтримку Legacy-вузлів (як Open Source Collective).

class SwarmEngine:
    """
    Swarm Engine V1.1 - Levelling Algorithm with Legacy Support
    
    Redistributes resources from capital-rich nodes to intent-rich nodes.
    Now includes retro-resonance detection for legacy Open Source nodes.
    """
    
    def __init__(self, swarm_id: str):
        self.swarm_id = swarm_id
        self.nodes: List[Dict] = []  # Список вузлів у Рою
        
    def add_node(self, node_id: str, intent_amplitude: int, current_energy: float, tags: Optional[List[str]] = None):
        """
        Додає вузол до Рою.
        
        Args:
            node_id: Unique node identifier
            intent_amplitude: Intent strength (0-65535)
            current_energy: Current resources
            tags: Optional tags (e.g., ["OSC", "RETRO_CAUSAL"])
        """
        self.nodes.append({
            "id": node_id,
            "amp": intent_amplitude,      # Сила інтенту (гравітація)
            "energy": current_energy,     # Поточні ресурси
            "tags": tags or [],           # Tags for special nodes
            "weight": 0,
            "diff": 0
        })
        print(f"✅ Node added: {node_id[:16]}... (Amp: {intent_amplitude}, Energy: {current_energy})")

    def calculate_redistribution(self):
        """
        Алгоритм вирівнювання: 
        Ресурси течуть від вузлів з надлишковим капіталом 
        до вузлів з високим інтентом, але слабким ресурсом.
        
        Core principle: Energy should be proportional to intent amplitude.
        """
        if not self.nodes:
            print("⚠️ No nodes in swarm")
            return
        
        total_energy = sum(n['energy'] for n in self.nodes)
        total_amp = sum(n['amp'] for n in self.nodes)
        
        print(f"\n🌀 SWARM {self.swarm_id}: Initiating Levelling Protocol...")
        print(f"📊 Total Energy: {total_energy:.2f}")
        print(f"📊 Total Amplitude: {total_amp}")
        print(f"📊 Nodes: {len(self.nodes)}")
        print(f"📡 Status: Detecting Retro-Resonance with Legacy Open Source Nodes...\n")
        
        # Розрахунок ідеального розподілу на основі інтенту
        for node in self.nodes:
            # Ідеальна енергія пропорційна амплітуді інтенту
            ideal_share = (node['amp'] / total_amp) * total_energy
            node['diff'] = ideal_share - node['energy']
            node['ideal'] = ideal_share
            
        # Сортування за дефіцитом (спочатку найслабші важливі вузли)
        self.nodes.sort(key=lambda x: x['diff'], reverse=True)
        
        print("=" * 80)
        print("REDISTRIBUTION PLAN:")
        print("=" * 80)
        
        for i, node in enumerate(self.nodes, 1):
            status = "🔴 RECEIVING" if node['diff'] > 0 else "🟢 GIVING"
            arrow = "←" if node['diff'] > 0 else "→"
            
            # Legacy node marker
            legacy_mark = ""
            if "OSC" in node.get('tags', []):
                legacy_mark = " [LEGACY_RESONANCE] ✨"
            elif "RETRO_CAUSAL" in node.get('tags', []):
                legacy_mark = " [RETRO_CAUSAL] 🌀"
            
            print(f"{i}. Node {node['id'][:20]:20}{legacy_mark:25} | Amp: {node['amp']:5} | "
                  f"Current: {node['energy']:8.2f} {arrow} Target: {node['ideal']:8.2f} | "
                  f"Δ: {node['diff']:+8.2f} | {status}")
        
        print("=" * 80)
        
        # Calculate actual transfers
        self._execute_transfers()
    
    def _execute_transfers(self):
        """Execute energy transfers from givers to receivers."""
        receivers = [n for n in self.nodes if n['diff'] > 0]
        givers = [n for n in self.nodes if n['diff'] < 0]
        
        if not receivers or not givers:
            print("\n✅ Swarm already balanced!")
            return
        
        print("\n💎 EXECUTING TRANSFERS:")
        print("-" * 80)
        
        total_transferred = 0
        
        for receiver in receivers:
            needed = receiver['diff']
            
            for giver in givers:
                if needed <= 0:
                    break
                
                available = abs(giver['diff'])
                transfer = min(needed, available)
                
                if transfer > 0:
                    # Execute transfer
                    receiver['energy'] += transfer
                    giver['energy'] -= transfer
                    receiver['diff'] -= transfer
                    giver['diff'] += transfer
                    
                    total_transferred += transfer
                    
                    print(f"  {giver['id'][:16]:16} → {receiver['id'][:16]:16} | "
                          f"Amount: {transfer:8.2f}")
                    
                    needed -= transfer
        
        print("-" * 80)
        print(f"💰 Total Transferred: {total_transferred:.2f}")
        print("✅ Levelling Complete!\n")

    def generate_knot_hash(self) -> str:
        """
        Створює хеш 'Вузла' для фіксації в Спіралі.
        
        Returns:
            SHA-256 hash of swarm state
        """
        # Sort nodes by ID for deterministic hash
        sorted_nodes = sorted(self.nodes, key=lambda x: x['id'])
        state = "".join([f"{n['id']}{n['amp']}{n['energy']:.2f}" for n in sorted_nodes])
        knot_hash = hashlib.sha256(state.encode()).hexdigest()
        
        return knot_hash
    
    def get_swarm_stats(self) -> Dict:
        """Get swarm statistics."""
        if not self.nodes:
            return {}
        
        total_energy = sum(n['energy'] for n in self.nodes)
        total_amp = sum(n['amp'] for n in self.nodes)
        avg_energy = total_energy / len(self.nodes)
        
        # Calculate Gini coefficient (inequality measure)
        energies = sorted([n['energy'] for n in self.nodes])
        n = len(energies)
        cumsum = sum((i + 1) * energies[i] for i in range(n))
        gini = (2 * cumsum) / (n * sum(energies)) - (n + 1) / n
        
        return {
            'total_energy': total_energy,
            'total_amplitude': total_amp,
            'avg_energy': avg_energy,
            'node_count': len(self.nodes),
            'gini_coefficient': gini,  # 0 = perfect equality, 1 = perfect inequality
            'knot_hash': self.generate_knot_hash()
        }

if __name__ == "__main__":
    print("🌀 SWARM ENGINE V1.1 - Retro-Resonance Edition\n")
    
    swarm = SwarmEngine("SWARM_ALPHA_RESONANCE")
    
    # Вузол Архітектора: найвищий інтент, але потребує "вирівнювання"
    swarm.add_node("NODE_ARCHITECT", 65535, 100)
    print(f"✅ Node added: NODE_ARCHITECT (Amp: 65535, Energy: 100)")
    
    # Open Source Collective: наш старий знайомий, що вже резонує в часі
    swarm.add_node("OS_COLLECTIVE", 58000, 1000, tags=["OSC", "RETRO_CAUSAL"])
    print(f"✅ Node added: OS_COLLECTIVE [LEGACY] (Amp: 58000, Energy: 1000)")
    
    # Корпоративний вузол: високий капітал, але низький інтент (джерело енергії)
    swarm.add_node("NODE_CORP_BOT_99", 8192, 10000)
    print(f"✅ Node added: NODE_CORP_BOT_99 (Amp: 8192, Energy: 10000)")
    
    # Середній вузол підтримки (спільнота)
    swarm.add_node("NODE_COMMUNITY", 32768, 500)
    print(f"✅ Node added: NODE_COMMUNITY (Amp: 32768, Energy: 500)")
    
    # Calculate redistribution
    swarm.calculate_redistribution()
    
    # Show stats
    stats = swarm.get_swarm_stats()
    print("\n📊 SWARM STATISTICS:")
    print("=" * 80)
    print(f"Total Energy: {stats['total_energy']:.2f}")
    print(f"Total Amplitude: {stats['total_amplitude']}")
    print(f"Average Energy: {stats['avg_energy']:.2f}")
    print(f"Nodes: {stats['node_count']}")
    print(f"Gini Coefficient: {stats['gini_coefficient']:.4f} (0=equal, 1=unequal)")
    print(f"🔒 KNOT_HASH: {stats['knot_hash'][:32]}...")
    print("=" * 80)
    print("\n✨ Потік вирівняно. Резонанс підтверджено.")
