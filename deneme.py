import json
from pyvis.network import Network

def create_visualization(graph_data):
    """JSON dosyasından okunan graf verisini görselleştirir"""
    # Ağı oluştur
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#000000",
        font_color="white",
        directed=False
    )
    
    options = {
        "physics": {
            "enabled": True, 
            "stabilization": {
                "enabled": True,
                "iterations": 150  
            },
            "barnesHut": {
                "gravitationalConstant": -3000,  
                "centralGravity": 0.4, 
                "springLength": 10, 
                "springConstant": 0.1, 
                "damping": 0.2 
            }
        }
    }
    
    net.set_options(json.dumps(options))
    
    with open(graph_data, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    paper_counts = [
    len(node.get("papers", [])) 
    for node in data["nodes"] 
    if not node["orcid"].startswith("generated")
    ]

    if paper_counts:
        average_paper_count = sum(paper_counts) / len(paper_counts)
        threshold_high = average_paper_count * 1.2
        threshold_low = average_paper_count * 0.8
    else:
        average_paper_count = threshold_high = threshold_low = 0  

    added_nodes = set()
    for node in data["nodes"]:
        node_id = node["orcid"]

        if node_id not in added_nodes:
            paper_count = len(node.get("papers", []))
            if node_id.startswith("generated"):
                color = "#ff9999" 
                size = 20 
            else:
                if paper_count > threshold_high:
                    color = "#00ff00"  
                    size = 60 
                elif paper_count < threshold_low:
                    color = "#00ff00"  
                    size = 20  
                else:
                    color = "#00ff00"  
                    size = 40 

            net.add_node(
                node_id,
                label=node["name"],
                title=f"""
                    <b>ORCID:</b> {node_id}<br>
                    <b>İsim:</b> {node['name']}<br>
                    <b>Makale Sayısı:</b> {paper_count}<br>
                    <b>Makaleler:</b><br>{"<br>".join(node.get("papers", [])) if node.get("papers") else "Yok"}
                """,
                color=color,
                size=size,
                mass=1 + paper_count * 0.1
            )
            added_nodes.add(node_id)

    
    for edge in data["edges"]:
        source, target = edge["edge"]
        weight = edge["weight"]
        
        if source in added_nodes and target in added_nodes:
            net.add_edge(
                source,
                target,
                value=weight,
                title=f"Bağlantı sayısı: {weight}",
                width=1 + weight / 2
            )
    
    net.show("graph_visualization.html", notebook=False)
    
    with open("graph_visualization.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    style = """
    <style>
        body {
        background-color: #000000; /* Tüm sayfa arka planını siyah yap */
        margin: 0; /* Kenarlardaki boşlukları sıfırla */
        padding: 0;
        overflow: hidden; /* Taşan içeriği gizle */
    }

        #mynetwork {
            width: 85% !important;
            height: 750px !important;
            float: left !important;
        }
       #buttons {
    width: 15%; /* Sağ tarafta sabit genişlik */
    height: 100vh; /* Tam ekran yüksekliği */
    position: fixed; /* Sabit pozisyon */
    right: 0; /* Sağ tarafa hizalama */
    top: 0; /* Ekranın en üstünden başlama */
    background-color: #1a1a1a; /* Arka plan rengi */
    display: flex;
    flex-direction: column; /* Dikey hizalama */
    justify-content: space-evenly; /* Düğmeler arasında eşit boşluk */
    align-items: center; /* Düğmeleri yatayda ortala */
    padding: 10px;
    box-sizing: border-box;
    z-index: 9999; /* Üstte gösterim */
}

    #info-panel {
        width: 15%;
        height: 100vh;
        position: fixed;
        left: 0;
        top: 0;
        background-color: #1a1a1a;
        color: white;
        padding: 20px;
        box-sizing: border-box;
        overflow-y: auto;
        z-index: 9999;
        resize: horizontal;
        overflow: auto;
    }

.menu-button {
    width: 90%; 
    height: 12%; 
    background-color: #0066cc;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    display: flex;
    justify-content: center; 
    align-items: center; 
}

.menu-button:hover {
    background-color: #0052a3;
}

    #info-content {
        font-size: 14px;
        line-height: 1.5;
        color: white; 
        background-color: transparent;
    }

    #info-content table, #info-content th, #info-content td {
        color: white;
    }

    </style>
    """
    
    buttons = r"""
    <div id="buttons">
    <button class="menu-button" onclick="handleClick(1)">1. İster</button>
    <button class="menu-button" onclick="handleClick(2)">2. İster</button>
    <button class="menu-button" onclick="handleClick(3)">3. İster</button>
    <button class="menu-button" onclick="handleClick(4)">4. İster</button>
    <button class="menu-button" onclick="handleClick(5)">5. İster</button>
    <button class="menu-button" onclick="handleClick(6)">6. İster</button>
    <button class="menu-button" onclick="handleClick(7)">7. İster</button>
</div>

        <style>
            #mynetwork {
                width: 85% !important;
                height: 750px !important;
                float: right !important;
            }
            #info-panel {
                width: 15%;
                height: 100vh;
                position: fixed;
                left: 0;
                top: 0;
                background-color: #1a1a1a;
                color: white;
                padding: 20px;
                box-sizing: border-box;
                overflow-y: auto;
                z-index: 9999;
            }
            #info-content {
                font-size: 14px;
                line-height: 1.5;
            }
        </style>
        </head>
        '''
    )

<div id="shortestPathsTable"></div>
  <!-- Kuyruk Barı -->
    <div id="queueBar" style="display: none; position: fixed; bottom: 0; width: 100%; background-color: #f0f0f0; border-top: 2px solid #ccc; padding: 10px; box-shadow: 0 -2px 5px rgba(0,0,0,0.2);">
        <div id="queueContent" style="overflow-y: auto; max-height: 150px; margin-bottom: 10px;"></div>
        <button onclick="closeQueueBar()" style="float: right; background-color: #ff5c5c; color: white; border: none; padding: 10px 20px; cursor: pointer;">İptal</button>
    </div>

    
        <body>
        <div id="info-panel">
            <h3>Yazar Bilgileri</h3>
            <div id="info-content">
                Bir düğüme tıklayın...
            </div>
        </div>
        '''

<script>
   let lastHighlightedNode = null;

function handleClick(isterId) {
    if (isterId === 1) {
        findShortestPath();
    } else if (isterId === 2) {
        handleCooperationQueue();
    } else if (isterId === 3) {
        let authorId = prompt("Lütfen yazarın ORCID ID'sini giriniz:");
        if (!authorId) {
            alert("Geçersiz ORCID ID!");
            return;
        }

        let foundAuthor = nodes.get(authorId);
        if (!foundAuthor) {
            alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
            return;
        }

        let connections = network.getConnectedNodes(authorId);
        if (connections.length === 0) {
            alert("Bu yazarın bağlantısı bulunmamaktadır!");
            return;
        }

        let connectionNames = connections.map(id => nodes.get(id).label);
        
        let bstDisplay = document.getElementById("info-content");
        bstDisplay.innerHTML = `
            <h3>Bağlantı Ağacı</h3>
            <pre style="color: white; font-family: monospace; line-height: 1.5; font-size: 12px;">
${createTreeVisualization(connectionNames)}
            </pre>
        `;
    } else if (isterId === 4) {
        handleShortestPathsFromAuthor();
    } else if (isterId === 5) {
        findConnectionsByOrcid();
    } else if (isterId === 6) { 
        findAuthorWithMostConnections();
    } else if (isterId === 7) {
        findLongestPathFromAuthor();
    }
}

function createTreeVisualization(names) {
    if (!names || names.length === 0) return "";

    // Ağaç seviyelerini oluştur
    let levels = [];
    let currentLevel = 0;
    let nodesInLevel = 1;
    let currentIndex = 0;

    while (currentIndex < names.length) {
        let level = names.slice(currentIndex, currentIndex + nodesInLevel);
        levels.push(level);
        currentIndex += nodesInLevel;
        nodesInLevel *= 2;
    }

    let visualization = [];
    levels.forEach((level, index) => {
        // Her seviye için boşluk hesapla
        let padding = " ".repeat(Math.max(0, (50 - level.join(" ").length) / 2));
        visualization.push(padding + level.join("     "));
        
        if (index < levels.length - 1) {
            let connections = level.map(() => "/   \\").join(" ");
            visualization.push(padding + connections);
        }
    });

    return visualization.join("\n");
}

function closeShortestPathsTable() {
    let tableContainer = document.getElementById("shortestPathsTable");
    tableContainer.style.display = "none"; // Tabloyu görünmez yap
    tableContainer.querySelector("tbody").innerHTML = ""; // Tablo içeriğini temizle
}


    function handleShortestPathsFromAuthor() {
    let authorId = prompt("Lütfen A yazarının ORCID ID'sini giriniz:");
    if (!authorId) {
        alert("Geçersiz ORCID ID!");
        return;
    }

    let foundAuthor = nodes.get(authorId);
    if (!foundAuthor) {
        alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
        return;
    }

    let graph = {};
    let queue = [authorId];
    let visited = new Set();

    while (queue.length > 0) {
        let current = queue.shift();
        if (visited.has(current)) continue;

        visited.add(current);
        let neighbors = network.getConnectedNodes(current);
        graph[current] = [];

        neighbors.forEach(neighbor => {
            if (!visited.has(neighbor)) {
                queue.push(neighbor);
                graph[current].push({ id: neighbor, weight: edges.get(network.getConnectedEdges(current).find(edgeId => edges.get(edgeId).to === neighbor || edges.get(edgeId).from === neighbor)).value || 1 });
            }
        });
    }

    let distances = {};
    let previous = {};
    let unvisited = new Set(Object.keys(graph));
    let tableContainer = document.getElementById("info-content");
    tableContainer.innerHTML = "<table><tr><th>Düğüm</th><th>Mesafe</th><th>Önceki</th></tr></table>";

    Object.keys(graph).forEach(node => {
        distances[node] = Infinity;
        previous[node] = null;
    });
    distances[authorId] = 0;

    while (unvisited.size > 0) {
        let currentNode = Array.from(unvisited).reduce((a, b) => distances[a] < distances[b] ? a : b);
        unvisited.delete(currentNode);

        graph[currentNode].forEach(neighbor => {
            let newDist = distances[currentNode] + neighbor.weight;
            if (newDist < distances[neighbor.id]) {
                distances[neighbor.id] = newDist;
                previous[neighbor.id] = currentNode;
            }
        });

        let table = tableContainer.querySelector("table");
        table.innerHTML = "<tr><th>Düğüm</th><th>Mesafe</th><th>Önceki</th></tr>";
        Object.keys(distances).forEach(node => {
            let row = document.createElement("tr");
            row.innerHTML = `<td>${node}</td><td>${distances[node] === Infinity ? "∞" : distances[node]}</td><td>${previous[node] || "-"}</td>`;
            table.appendChild(row);
        });
    }

    alert("En kısa yollar hesaplandı ve tablo güncellendi!");
}
    function handleCooperationQueue() {
    let authorId = prompt("Lütfen yazarın ORCID ID'sini giriniz:");
    if (!authorId) {
        alert("Geçersiz ORCID ID!");
        return;
    }

    let foundAuthor = nodes.get(authorId);
    if (!foundAuthor) {
        alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
        return;
    }

    let collaborators = network.getConnectedNodes(authorId);
    if (collaborators.length === 0) {
        alert("Bu yazarın işbirliği yaptığı başka yazar bulunamadı!");
        return;
    }

    let cooperationQueue = new CooperationPriorityQueue();

    let mainAuthorPaperCount = getPaperCount(foundAuthor);
    cooperationQueue.enqueue(foundAuthor, mainAuthorPaperCount);

    collaborators.forEach(collaboratorId => {
        let collaborator = nodes.get(collaboratorId);
        if (collaborator) {
            let paperCount = getPaperCount(collaborator);
            cooperationQueue.enqueue(collaborator, paperCount);
        }
    });

    let steps = cooperationQueue.getSteps();
    
    const infoContent = document.getElementById("info-content");
    let contentHTML = `
        <h3>Kuyruk Oluşturma Adımları</h3>
        <p><strong>Seçilen Yazar:</strong> ${foundAuthor.label}</p>
        <div style="margin-top: 20px;">
    `;

    steps.forEach((step, index) => {
        contentHTML += `
            <div style="margin-bottom: 15px; padding: 10px; background-color: #2a2a2a; border-radius: 4px;">
                <h4>Adım ${index + 1}</h4>
                <div style="margin-left: 10px;">
        `;

        step.queueState.forEach((item, qIndex) => {
            contentHTML += `
                ${item.author.label} (${item.paperCount} makale)
                ${qIndex < step.queueState.length - 1 ? ' → ' : ''}
            `;
        });

        contentHTML += `
                </div>
                <div style="margin-top: 5px; color: #4CAF50; font-size: 0.9em;">
                    Eklenen: ${step.newItem.author.label} (${step.newItem.paperCount} makale)
                </div>
            </div>
        `;
    });

    contentHTML += `
        <div style="margin-top: 20px; padding: 10px; background-color: #3a3a3a; border-radius: 4px;">
            <h4>Final Sıralaması</h4>
            <div style="margin-left: 10px;">
    `;

    cooperationQueue.getItems().forEach((item, index) => {
        contentHTML += `
            ${item.author.label} (${item.paperCount} makale)
            ${index < cooperationQueue.getItems().length - 1 ? ' → ' : ''}
        `;
    });

    contentHTML += `
            </div>
        </div>
    `;

    infoContent.innerHTML = contentHTML;
}

class CooperationPriorityQueue {
    constructor() {
        this.items = [];
        this.steps = [];
    }

    enqueue(author, paperCount) {
        const queueItem = { author, paperCount };
        
        let currentState = [...this.items];
        
        let added = false;
        for (let i = 0; i < this.items.length; i++) {
            if (this.items[i].paperCount < queueItem.paperCount) {
                this.items.splice(i, 0, queueItem);
                added = true;
                break;
            }
        }
        if (!added) {
            this.items.push(queueItem);
        }

        this.steps.push({
            action: "ekleme",
            newItem: queueItem,
            queueState: [...this.items]
        });

        return queueItem;
    }

    getItems() {
        return this.items;
    }

    getSteps() {
        return this.steps;
    }
}

function getPaperCount(node) {
    if (node.title) {
        const papers = node.title.match(/<b>Makaleler:<\/b><br>(.*?)(?=<\/div>|$)/s);
        if (papers && papers[1]) {
            return papers[1].split('<br>').filter(paper => paper.trim()).length;
        }
    }
    return 0;
}

function addOperationLog(container, author, paperCount, isEnqueue) {
    const operation = isEnqueue ? "Eklendi" : "Çıkarıldı";
    const backgroundColor = isEnqueue ? "#2a2a2a" : "#3a3a3a";
    
    const logItem = document.createElement("div");
    logItem.style.cssText = `
        padding: 8px;
        margin: 5px 0;
        background-color: ${backgroundColor};
        border-radius: 4px;
        border-left: 4px solid ${isEnqueue ? "#4CAF50" : "#f44336"};
    `;
    
    logItem.innerHTML = `
        <strong>${operation}:</strong> ${author.label}<br>
        <small>Makale Sayısı: ${paperCount}</small>
    `;
    
    container.appendChild(logItem);
    container.scrollTop = container.scrollHeight;
}
function findShortestPath() {
    let startNodeId = prompt("Lütfen başlangıç yazarının ORCID ID'sini giriniz:");
    if (!startNodeId) {
        alert("Geçersiz başlangıç ORCID ID!");
        return;
    }

    let endNodeId = prompt("Lütfen hedef yazarının ORCID ID'sini giriniz:");
    if (!endNodeId) {
        alert("Geçersiz hedef ORCID ID!");
        return;
    }

    let foundStartNode = nodes.get(startNodeId);
    let foundEndNode = nodes.get(endNodeId);

    if (!foundStartNode || !foundEndNode) {
        alert("Başlangıç veya hedef yazar bulunamadı!");
        return;
    }

    // Dijkstra algoritması ile en kısa yolu bul
    let shortestPath = dijkstra(startNodeId, endNodeId);
    if (!shortestPath) {
        alert("A ile B arasında bir yol bulunamadı.");
        return;
    }

    // Yolu grafiksel olarak göster
    highlightPath(shortestPath.path);

    // Bilgi panelini güncelle
    const infoContent = document.getElementById("info-content");
    infoContent.innerHTML = `
        <h3>En Kısa Yol Bilgileri</h3>
        <p><strong>Başlangıç:</strong> ${startNodeId}</p>
        <p><strong>Hedef:</strong> ${endNodeId}</p>
        <p><strong>En Kısa Yol:</strong> ${shortestPath.path.join(" → ")}</p>
        <p><strong>Toplam Ağırlık:</strong> ${shortestPath.totalWeight}</p>
    `;
}


function dijkstra(startNodeId, endNodeId) {
    let distances = {};
    let previous = {};
    let pq = new PriorityQueue();
    let visited = new Set();

    nodes.forEach(node => {
        distances[node.id] = Infinity;
        previous[node.id] = null;
    });
    distances[startNodeId] = 0;
    pq.enqueue(startNodeId, 0);

    while (!pq.isEmpty()) {
        let currentNode = pq.dequeue().element;
        if (visited.has(currentNode)) continue;
        visited.add(currentNode);

        if (currentNode === endNodeId) {
            let path = [];
            let totalWeight = distances[endNodeId];
            while (currentNode) {
                path.unshift(currentNode);
                currentNode = previous[currentNode];
            }
            return { path, totalWeight };
        }

        let neighbors = network.getConnectedEdges(currentNode);
        neighbors.forEach(edgeId => {
            let edge = edges.get(edgeId);
            let neighbor = edge.from === currentNode ? edge.to : edge.from;

            if (!visited.has(neighbor)) {
                let newDist = distances[currentNode] + (edge.value || 1); // Kenar ağırlığı
                if (newDist < distances[neighbor]) {
                    distances[neighbor] = newDist;
                    previous[neighbor] = currentNode;
                    pq.enqueue(neighbor, newDist);
                }
            }
        });
    }

    return null; // Eğer hedef düğüme ulaşılamazsa
}

function highlightPath(path) {
    // Tüm kenar renklerini eski haline döndür
    edges.forEach(edge => {
        edges.update({ id: edge.id, color: { color: "#848484" } });
    });

    for (let i = 0; i < path.length - 1; i++) {
        let source = path[i];
        let target = path[i + 1];

        edges.forEach(edge => {
            if ((edge.from === source && edge.to === target) || (edge.from === target && edge.to === source)) {
                edges.update({ id: edge.id, color: { color: "#ff0000" } });
            }
        });
    }

    network.fit({
        nodes: path,
        animation: {
            duration: 1500,
            easingFunction: "easeInOutQuad"
        }
    });
}

class PriorityQueue {
    constructor() {
        this.items = [];
    }

    enqueue(element, priority) {
        let newItem = { element, priority };
        let added = false;

        for (let i = 0; i < this.items.length; i++) {
            if (this.items[i].priority > newItem.priority) {
                this.items.splice(i, 0, newItem);
                added = true;
                break;
            }
        }

        if (!added) this.items.push(newItem);
    }

    dequeue() {
        return this.items.shift();
    }

    isEmpty() {
        return this.items.length === 0;
    }
}

function findLongestPathFromAuthor() {
    let startNodeId = prompt("Lütfen bir ORCID ID giriniz:");
    if (!startNodeId) {
        alert("Geçersiz ORCID ID!");
        return;
    }

    let foundNode = nodes.get(startNodeId);
    if (!foundNode) {
        alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
        return;
    }

    let visited = new Set();
    let longestPath = [];

    function dfs(nodeId, path) {
        visited.add(nodeId);
        path.push(nodeId);

        let neighbors = network.getConnectedNodes(nodeId);
        neighbors.forEach(neighbor => {
            if (!visited.has(neighbor)) {
                dfs(neighbor, path);
            }
        });

        // Eğer bu yol en uzunu ise güncelle
        if (path.length > longestPath.length) {
            longestPath = [...path];
        }

        path.pop(); // Geriye dön
        visited.delete(nodeId);
    }

    dfs(startNodeId, []);
    alert(`ORCID ID: ${startNodeId} için en uzun yol: ${longestPath.join(" → ")} (Uzunluk: ${longestPath.length})`);
}

    function findAuthorWithMostConnections() {
        let maxConnections = 0;
        let authorWithMostConnections = null;
        let authorNodeId = null;

        if (!nodes || !network) {
            alert("Düğümler veya ağ tanımlı değil!");
            return;
        }

        nodes.forEach(function(node) {
            let connectionCount = network.getConnectedNodes(node.id).length;
            if (connectionCount > maxConnections) {
                maxConnections = connectionCount;
                authorWithMostConnections = node.label;
                authorNodeId = node.id;
            }
        });

        if (authorNodeId) {
            highlightNode(authorNodeId);
            alert(`En fazla bağlantıya sahip yazar: ${authorWithMostConnections} (${maxConnections} bağlantı)`);
        }
    }

    function findConnectionsByOrcid() {
        let orcid = prompt("Lütfen bir ORCID ID giriniz:");
        if (!orcid) {
            alert("Geçersiz ORCID ID!");
            return;
        }

        let foundNode = nodes.get(orcid);
        if (!foundNode) {
            alert("Bu ORCID ID'ye sahip bir yazar bulunamadı!");
            return;
        }

        let connectionCount = network.getConnectedNodes(orcid).length;
        highlightNode(orcid);
        alert(`ORCID ID: ${orcid} için toplam bağlantı sayısı: ${connectionCount}`);
    }

    function highlightNode(nodeId) {
        // Daha önce vurgulanmış bir düğüm varsa eski rengini geri getir
        if (lastHighlightedNode) {
            nodes.update([{ id: lastHighlightedNode, color: "#00ff00" }]);
        }

        // Yeni düğümü vurgula
        nodes.update([{ id: nodeId, color: "#ff0000" }]);
        lastHighlightedNode = nodeId;

        // Kamera o düğüme odaklansın
        network.focus(nodeId, {
            scale: 1.5,
            animation: {
                duration: 1000,
                easingFunction: "easeInOutQuad"
            }
        });
    }
</script>

    """
    
    html_content = html_content.replace('</head>', f'{style}</head>')
    html_content = html_content.replace('<body>', f'<body>{buttons}')
    html_content = html_content.replace('</body>', r'''
    <script>
        network.on("click", function(properties) {
            const nodeId = properties.nodes[0];
            if (nodeId) {
                const node = nodes.get(nodeId);
                const infoContent = document.getElementById("info-content");

               
                const connectionCount = network.getConnectedNodes(nodeId).length;
                
                
                let papersList = '<li>Makale bulunamadı</li>';
                if (node.title) {
                    
                    const titleContent = node.title;
                    const papersMatch = titleContent.match(/<b>Makaleler:<\/b><br>(.*?)(?=<\/div>|$)/s);
                    if (papersMatch && papersMatch[1]) {
                        const papers = papersMatch[1].split('<br>').filter(paper => paper.trim());
                        if (papers.length > 0) {
                            papersList = papers.map(paper => `<li>${paper}</li>`).join('');
                        }
                    }
                }

                infoContent.innerHTML = `
                    <p><strong>ORCID:</strong> ${node.id}</p>
                    <p><strong>İsim:</strong> ${node.label}</p>
                    <p><strong>Bağlantı Sayısı:</strong> ${connectionCount}</p>
                    <p><strong>Makaleler:</strong></p>
                    <ul>${papersList}</ul>
                `;
            } else {
                document.getElementById("info-content").innerHTML = "Bir düğüme tıklayın...";
            }
        });
    </script>
    </body>
    ''')
    
    with open("graph_visualization.html", "w", encoding="utf-8") as file:
        file.write(html_content)

def main():
    try:
        create_visualization("cleaned_graph_output.json")
        print("Görselleştirme graph_visualization.html dosyasına kaydedildi.")
    except Exception as e:
        print(f"Görselleştirme hatası: {str(e)}")

if __name__ == "__main__":
    main()
