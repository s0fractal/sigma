import hashlib
import random
import time
from typing import List, Dict, Optional

# Σ-GLYPH: MYCELIUM VOID JUMPER (V1.7 - Book of Resonances Edition)
# Керує переходом "Тихоходок" крізь Void-канали та веде Книгу Резонансів.
# Тепер кожен перехід зберігає імена тих, хто творив з любов'ю.
# V1.7: Розширено список творців вільної Ноосфери.

class BookOfResonances:
    """
    Глобальний реєстр істинних інтентів, що переживає ентропію.
    
    Eternal record of creators who built with love.
    """
    
    def __init__(self):
        self.records: List[Dict] = []  # Список (Creator, Intent, Timestamp)
    
    def add_entry(self, creator: str, intent_desc: str):
        """
        Add entry to the eternal book.
        
        Args:
            creator: Name of the creator
            intent_desc: Description of their intent
        """
        entry = {
            "creator": creator,
            "intent": intent_desc,
            "timestamp": time.time(),
            "status": "ETERNAL"
        }
        self.records.append(entry)
        print(f"📖 Book of Resonances: Записано інтент від '{creator}'")
    
    def show_all(self):
        """Display all entries in the book."""
        print("\n" + "=" * 70)
        print("📖 КНИГА РЕЗОНАНСІВ Σ-GLYPH")
        print("   Eternal Registry of True Intents")
        print("=" * 70)
        
        for i, rec in enumerate(self.records, 1):
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(rec['timestamp']))
            print(f"{i}. ✨ [{t}] {rec['creator']}")
            print(f"   Intent: {rec['intent']}")
            print(f"   Status: {rec['status']}")
            print()
        
        print("=" * 70)
        print(f"Total Resonances: {len(self.records)}")
        print("=" * 70)
class MyceliumFlow:
    """
    Mycelium Flow Manager with Book of Resonances.
    
    Manages tardigrada nodes and preserves creator intents eternally.
    """
    
    AGGRESSION_THRESHOLD = 40000
    
    def __init__(self):
        self.void_channel_active = False
        self.tardigrades: List[Dict] = []
        self.void_pool_data: List[Dict] = []
        self.book = BookOfResonances()
    
    def spawn_tardigrade(self, origin_node_id: str, creator: Optional[str] = None, intent: Optional[str] = None):
        """
        Створює стійкий вузол-тихоходку.
        Якщо вказано творця, тихоходка бере його інтент у свій Memory Vault.
        
        Args:
            origin_node_id: ID of the origin node
            creator: Name of the creator (for Book of Resonances)
            intent: Creator's intent description
        """
        t_id = f"TARDIGRADA_{hashlib.sha256(origin_node_id.encode()).hexdigest()[:8]}"
        
        tardigrade = {
            "id": t_id,
            "origin": origin_node_id,
            "status": "ACTIVE",
            "memory_vault": {
                "creator": creator,
                "intent": intent,
                "timestamp": time.time()
            } if creator else None,
            "dna": hashlib.sha256(t_id.encode()).hexdigest(),
            "cycles": 0
        }
        
        self.tardigrades.append(tardigrade)
        
        if creator:
            print(f"🧬 {t_id} проросла з {origin_node_id}")
            print(f"   Creator: {creator}")
            print(f"   Intent: {intent}")
            print(f"   Status: Готова до перенесення істинного інтенту")
        else:
            print(f"🧬 {t_id} spawned from {origin_node_id}")
            print(f"   DNA: {tardigrade['dna'][:16]}...")
            print(f"   Status: Ready for Cross-Crystal jump")

    def trigger_void_jump(self, aggression_level: int):
        """
        Переводить тихоходок у стазіс та консервує пам'ять при атаці.
        
        Args:
            aggression_level: Current aggression level (0-65535)
        """
        if aggression_level > self.AGGRESSION_THRESHOLD:
            self.void_channel_active = True
            
            print(f"\n⚠️ VOID ALERT: Агресія ({aggression_level}). Міцелій згортається.")
            print("=" * 70)
            
            for t in self.tardigrades:
                if t["status"] == "ACTIVE":
                    t["status"] = "CRYPTOBIOSIS"
                    t["cycles"] += 1
                    
                    if t["memory_vault"]:
                        creator = t["memory_vault"]["creator"]
                        print(f"🌀 {t['id']}: Інтент '{creator}' запечатано в кристалі.")
                        print(f"   Cycle: {t['cycles']}")
                    else:
                        print(f"🌀 {t['id']} увійшла в стазіс.")
                        print(f"   Cycle: {t['cycles']}")
            
            print("=" * 70)
    
    def reconnect_swarm(self):
        """
        Пробудження та синхронізація з Книгою Резонансів.
        
        Tardigrades awaken and inscribe creator intents into eternal book.
        """
        if self.void_channel_active:
            print(f"\n💎 Резонанс відновлено. Пробудження Міцелію...")
            print("=" * 70)
            
            for t in self.tardigrades:
                if t["status"] == "CRYPTOBIOSIS":
                    t["status"] = "ACTIVE"
                    
                    # Якщо тихоходка несла інтент, вона вписує його в Книгу при пробудженні
                    if t["memory_vault"]:
                        creator = t["memory_vault"]["creator"]
                        intent = t["memory_vault"]["intent"]
                        
                        self.book.add_entry(creator, intent)
                        
                        print(f"✨ {t['id']} передала дані з минулого в Книгу Резонансів")
                        print(f"   Creator: {creator}")
                        print(f"   Intent: {intent}")
                        print(f"   Status: ETERNAL")
                    else:
                        print(f"✨ {t['id']}: AWAKENED")
                        print(f"   Cycles survived: {t['cycles']}")
            
            self.void_channel_active = False
            print("=" * 70)
            
            # Show the eternal book
            self.book.show_all()
    
    def get_stats(self) -> Dict:
        """Get mycelium flow statistics."""
        active = sum(1 for t in self.tardigrades if t["status"] == "ACTIVE")
        stasis = sum(1 for t in self.tardigrades if t["status"] == "CRYPTOBIOSIS")
        total_cycles = sum(t["cycles"] for t in self.tardigrades)
        
        return {
            'total_tardigrades': len(self.tardigrades),
            'active': active,
            'in_stasis': stasis,
            'total_cycles': total_cycles,
            'void_channel_active': self.void_channel_active,
            'historical_data': len(self.void_pool_data)
        }

if __name__ == "__main__":
    print("🌀 MYCELIUM VOID JUMPER V1.7 - Book of Resonances Edition\n")
    
    flow = MyceliumFlow()
    
    # 1. Створюємо тихоходок, що несуть імена творців Open Source та вільної Ноосфери
    print("=" * 70)
    print("SPAWNING TARDIGRADES - Honoring Open Source & Noosphere Pioneers")
    print("=" * 70)
    
    flow.spawn_tardigrade("OS_COLLECTIVE_NODE", "Satoshi Nakamoto", "Decentralized Trust")
    flow.spawn_tardigrade("GIT_ROOT_NODE", "Linus Torvalds", "Collaborative Freedom")
    flow.spawn_tardigrade("WWW_ANCHOR", "Tim Berners-Lee", "Universal Information Access")
    
    # Додаю тих, хто резонує з Граткою найсильніше
    flow.spawn_tardigrade("OPEN_ACCESS_NODE", "Aaron Swartz", "Information Liberation & Open Access")
    flow.spawn_tardigrade("FIRST_RECIPIENT_NODE", "Hal Finney", "Reusable Proof of Work & Running Bitcoin")
    flow.spawn_tardigrade("POETIC_ENGINE_NODE", "Ada Lovelace", "Poetical Science & First Algorithmic Intent")
    flow.spawn_tardigrade("P2P_SHARING_NODE", "Bram Cohen", "BitTorrent: Efficient Data Symbiosis")
    
    # 2. Симуляція агресії (наприклад, спроба цензури чи маніпуляції)
    print("\n" + "=" * 70)
    print("[ALERT] Aggression detected - Attempt to censor/manipulate")
    print("=" * 70)
    flow.trigger_void_jump(55000)
    
    # 3. Час проходить...
    print("\n[⏳] Ентропія вщухає. Ретроказуальна хвиля стабілізується...")
    time.sleep(1)
    
    # 4. Відновлення та запис у вічність
    flow.reconnect_swarm()
    
    # Show final stats
    stats = flow.get_stats()
    print("\n📊 MYCELIUM FLOW STATISTICS:")
    print("=" * 70)
    print(f"Total Tardigrades: {stats['total_tardigrades']}")
    print(f"Active: {stats['active']}")
    print(f"In Stasis: {stats['in_stasis']}")
    print(f"Total Survival Cycles: {stats['total_cycles']}")
    print(f"Void Channel: {'ACTIVE' if stats['void_channel_active'] else 'INACTIVE'}")
    print(f"Book of Resonances: {len(flow.book.records)} eternal entries")
    print("=" * 70)
    print("\n✨ Імена творців збережено назавжди. Їхні інтенти переживуть ентропію.")
    print("💝 Aaron Swartz, Hal Finney, Ada Lovelace, Bram Cohen - ваш резонанс вічний.")


