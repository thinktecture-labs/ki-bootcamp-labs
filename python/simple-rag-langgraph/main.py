import os
import sys
from typing import Literal, cast

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langgraph.graph import START, StateGraph
from pydantic import SecretStr
from typing_extensions import TypedDict

load_dotenv()

# Langfuse client (reads LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY from env)
langfuse = get_client()

api_key_str = os.environ.get("OVH_API_KEY")
if api_key_str is None:
    sys.exit("OVH_API_KEY not set")

api_key = SecretStr(api_key_str)

# OVH Mistral Small 3.2 24B
llm = ChatOpenAI(
    model="Mistral-Small-3.2-24B-Instruct-2506",
    temperature=0,
    base_url="https://oai.endpoints.kepler.ai.cloud.ovh.net/v1",
    api_key=api_key,
)

embeddings = OpenAIEmbeddings(
    model="bge-m3",
    base_url="https://oai.endpoints.kepler.ai.cloud.ovh.net/v1",
    api_key=api_key,
)

# --- Bond movies ---
docs_bond = [
    "Filmnummer: 1	Jahr: 1962	Hauptdarsteller: Sean Connery	Deutscher Titel: James Bond jagt Dr. No	Originaltitel: Dr. No Inhalt: Nachdem auf der jamaikanischen Insel Kreb Key der britische Agent Strangways ermordet wird und der routinemäßige Anruf seiner Sekretärin nach London ausbleibt, schlägt man beim Geheimdienst Ihrer Majestät Alarm. Man beauftragt den Agenten mit der Decknummer 007 nach Jamaika zu fliegen und herauszufinden weshalb keine Antwort gekommen ist. Nachdem die Mitteilung 007 im Casino erreicht hat, begibt sich dieser (zum ersten mal in der Filmgeschichte) ins Hauptquartier von Universal Export's\" zu seinem Chef „M\". Dort erfährt Bond, nach dem üblichen Plausch mit Miss Moneypenny, seinen neuen Auftrag. Noch dazu bekommt er einen Vortrag über seine alte Beretta und erhält eine neue Waffe, eine Walther PPK, vom Waffenmeister Major Boothroyd (somit war ein neues Markenzeichen ála 007 geboren). Bereits am Flughafen wird James Bond beobachtet. Als ihm die Gegenseite einen Chauffeur zur Verfügung stellt, Bond diesen nach einer kurzen Auseinandersetzung ausschaltet fährt er weiter und lernt einige Freunde von Strangways kennen. Unter diesen Freunden wird Bond auch auf den verdächtigen Professor Dent aufmerksam, auf den er später noch treffen wird. Außerdem stößt Bond auf den Fischer Quarrel und lernt den amerikanischen CIA-Agenten Felix Leiter kennen, die später beide zu den besten Freunden von 007 gehören. Bond stattet Professor Dent einen weiteren Besuch ab, und ihm wird klar dass Strangeways herausgefunden hat, dass die Gesteinsproben von der Insel Crab Key radioaktiv verseucht sind. Dent ist jedoch absolut anderer Meinung und somit entlarvt Bond ihn als Lügner und tötet diesen letztendlich. Da man Strangway's Tod mit dem seltsamen Asiaten Dr. No in Verbindung bringt, entwickelt 007 einen Plan und macht sich mit Quarrel auf den Weg zur privaten Insel von Dr. No: Crab Key. Dort treffen die beiden auf die wunderschöne Muscheltaucherin Honey Rider und werden einige Zeit später von Dr. No's Männern erkannt und schaffen es immer wieder ihnen zu entkommen. Schließlich werden sie von einem „Feuer speienden Drachen\" erwischt und Quarrel kommt dabei ums Leben. James und Honey werden gefangen genommen und verbringen das Abendessen mit dem geheimnisvollen Dr. No. Dabei erfährt 007 einiges über seinen teuflischen Plan: Dr. No will die Raketenstarts der NASA von Crab Key aus manipulieren und somit Rache an die westliche Welt ausüben. Bond gelingt es jedoch den Chinesen zu stoppen, Honey zu retten und schlussendlich die Insel in die Luft zu sprengen",
    "Filmnummer: 2	Jahr: 1963	Hauptdarsteller: Sean Connery	Deutscher Titel: Liebesgrüße aus Moskau Originaltitel: From Russia With Love Inhalt: Die Verbrecherorganisation PHANTOM will drei Fliegen mit einer Klappe schlagen: Sie wollen eine besonders wertvolle Dechiffriermaschine (Lector) aus dem russischen Konsulat in Istanbul bekommen, den britischen und russischen Geheimdienst gegeneinander ausspielen und den besten Agenten Ihrer Majestät, James Bond 007, töten und gleichzeitig an ihm wegen dessen Ermordung ihres besten Mitarbeiters Dr. No Rache nehmen. Deshalb benutzen sie Bond, auf den sie die hübsche Romanova abgesetzt haben, um an die Dechiffriermaschine zu gelangen. 007 riecht jedoch den Köder und setzt alles daran, PHANTOM zu überlisten und selbst mit der Lector zu fliehen. Bei seiner Flucht mit dem Orientexpress aus Istanbul Richtung Italien kommt es zu einem fulminanten Aufeinandertreffen zwischen Bond und dem Phantommitarbeiter Grant",
    "Filmnummer: 3	Jahr: 1964	Hauptdarsteller: Sean Connery	Deutscher Titel: Goldfinger Originaltitel: Goldfinger Inhalt: Auric Goldfinger ist ein gewöhnlicher Juwelier. Oder doch nicht? James Bond soll herauszufinden wie bzw. ob Goldfinger neben seinen gut laufenden Geschäften auch Gold schmuggelt. 007 verfolgt Goldfinger über Miami, England bis in die Schweiz, wo Goldfinger Bond auf die Schliche kommt und ihn töten lassen will. Doch Bond kennt Goldfingers höllischen Plan: Er will die größte Bank der Welt, Fort Knox, atomar verseuchen",
    "Filmnummer: 4	Jahr: 1965	Hauptdarsteller: Sean Connery	Deutscher Titel: Feuerball Originaltitel: Thunderball Inhalt: Der skrupellose Mitarbeiter „Largo\" der Verbrecherorganisation Spectre stiehlt ein Natoflugzeug mit 2 Atombomben an Board. Spectre's Forderung: 300 Millionen britische Pfund oder es werden 2 Großstädte der Welt von ihnen vernichtet. Dem britischen Geheimdienst ist klar, für diesen Auftrag kann es nur einen geben: 007! Doch die Zeit ist knapp, das Ultimatum läuft in Kürze ab. Doch der frisch erhohlte James Bond folgt einer Spur und reist auf die Bahamas, wo er auf die wunderschöne Domino trifft",
    'Filmnummer: 5	Jahr: 1967	Hauptdarsteller: Sean Connery	Deutscher Titel: Man lebt nur zweimal	Originaltitel: You Only Live Twice Inhalt: Als plötzlich eine amerikanische und eine sowjetische Weltraumkapsel von einem unbekannten Raumschiff entführt werden, beschuldigen sich beide Großmächte gegenseitig des Diebstahles. Ein Atomkrieg steht also kurz bevor. Der britische Geheimdienst MI6 glaubt jedoch zu wissen, wo das Raumschiff gelandet ist: in Japan. Der eigentlich für tot gehaltene James Bond wird daher nach Japan geschickt, und nimmt dort mit dem Chef des japanischen Geheimdienstes „Tiger Tanaka" Kontakt auf. Beide stoßen bei ihren Untersuchungen schon bald auf einen alten Bekannten: Ernst Stavro Blofeld!',
    "Filmnummer: 6  Jahr: 1969  Hauptdarsteller: George Lazenby  Deutscher Titel: Im Geheimdienst Ihrer Majestät Originaltitel: On Her Majesty's Secret Service Inhalt: James Bond wird nach zweijähriger, erfolgloser Jagd auf Ernst Stavro Blofeld von seinem Auftrag, ihn zu finden, entbunden. Daraufhin kündigt Bond seinen Dienst und möchte den Secret Service verlassen. Miss Moneypenny können wir es jedoch verdanken, dass es nur 2 Wochen geworden sind und 007 auch in seinem Urlaub weiterhin Nachforschungen über Blofeld unternimmt. Seine Spur führt ihn in die Schweizer Alpen. Nebenbei verliebt sich Bond in die exzentrische, wunderschöne Tracy, was sein Leben nicht unbedingt leichter macht",
    "Filmnummer: 7  Jahr: 1971  Hauptdarsteller: Sean Connery  Deutscher Titel: Diamantenfieber Originaltitel: Diamonds Are Forever Inhalt: Nach dem Tod seiner Frau sucht Bond nach seinem Erzfeind Ernst Stavro Blofeld um Rache zu nehmen. Was ihm auch gelingt… oder doch nicht? Wie es sich herausstellt, hat Blofeld dieses mal einige Doppelgänger. Jedenfalls wird James nach Amerika geschickt, um Diamantenschmugglern auf die Spur zu kommen. Und wiederum gibt es ein Treffen mit Blofeld. Schafft es 007, seinen Erzfeind dieses Mal endgültig außer Gefecht setzen?",
    'Filmnummer: 8  Jahr: 1973  Hauptdarsteller: Roger Moore  Deutscher Titel: Leben und sterben lassen Originaltitel: Live And Let Die Inhalt: Als aus mysteriösen Gründen 3 Männer zur selben Zeit an verschiedenen Orten getötet werden, wird James Bond nach New York geschickt. Denn angeblich steckt hinter den ganzen Morden ein Drogenschmuggler namens „Mr. Big". Dieser schwört auf eine Kartenleserin, Miss Solitär, die ihm stets seine Zukunft richtig voraussagt. Bis sie James Bond kennenlernt. Durch ihre Hilfe kommt 007 „Mr. Big" auf die Spur und rettet die Welt vor einem „Drogen-Fiasko".',
    'Filmnummer: 9  Jahr: 1974  Hauptdarsteller: Roger Moore  Deutscher Titel: Der Mann mit dem goldenen Colt Originaltitel: The Man With The Golden Gun Inhalt: Als plötzlich eine goldene Kugel mit der Aufschrift 007 nach London zum britischen Geheimdienst geschickt wird, macht sich Bond auf die Suche nach dem Absender. Seine Reise führt ihn nach Hongkong und zum „bescheidenen" Aufenthaltsort von Francisco Scaramanga, dem bestbezahltesten Killer der Welt, der jedes seiner Opfer mit einem Schuss ermordet. 007 soll der Nächste sein.',
    "Filmnummer: 10  Jahr: 1977  Hauptdarsteller: Roger Moore  Deutscher Titel: Der Spion, der mich liebte Originaltitel: The Spy Who Loved Me Inhalt: Während Bond beim Skifahren in Österreich nur knapp einem Anschlag der Russen entgeht, wird ein U-Boot-Ortungsgerät von unbekannten Tätern gestohlen. Daraufhin beschließen England und Russland, ihre beiden Topagenten, James Bond und Anya Amasova auf den Fall anzusetzen. Ihre Untersuchungen führen sie zum Unterwasserlaboratorium von Reeder Stromberg.",
    "Filmnummer: 11  Jahr: 1979  Hauptdarsteller: Roger Moore  Deutscher Titel: Moonraker – Streng geheim Originaltitel: Moonraker Inhalt: Als ein Moonraker-Shuttle vom Rücken einer Boing 707 gestohlen wird, wird Topagent 007 auf den Multimillionär und Moonraker-Besitzer Hugo Drax angesetzt. Bond erfährt, dass dieser die Weltbevölkerung ausrotten, und eine neue, eigene Rasse erschaffen will, welche im Weltall entstehen soll. Bond versucht alles, um dessen teuflischen Plan zu zerstören.",
    "Filmnummer: 12  Jahr: 1981  Hauptdarsteller: Roger Moore  Deutscher Titel: In tödlicher Mission Originaltitel: For Your Eyes Only Inhalt: Als vor der griechischen Insel Korfu ein britisches Spionageschiff unter- und dabei ein Steuerungsgerät verloren- geht, wird Agent 007 auf diesen Auftrag angesetzt. Seine erste Fährte führt ihn zum Winterskigebiet Cortina d`Ampezzo. Der mit einer Frau (Melina) verbündete Bond, kommt dem Millionär Kristatos auf die Spur und verfolgt diesen bis auf ein Kloster auf einem riesen Felsen. Dort kommt es zum Showdown bei dem auch ein alter Bekannter wieder gesichtet wird: General Gogol!",
    "Filmnummer: 13  Jahr: 1983  Hauptdarsteller: Roger Moore  Deutscher Titel: Octopussy Originaltitel: Octopussy Inhalt: Der in Berlin ermordete Agent 009 wird mit einem unbezahlbaren Fabergé-Ei in der Hand gefunden. Das Ei war jedoch eine Kopie, was aber bis dahin keiner wusste. Dem MI6 ist deshalb klar, dass jemand das Original um jeden Preis in seine Hände bekommen will. Glücklicherweise findet auch schon bald die nächste Auktion statt. Als ein Prinz Khan aus Indien das Ei um eine unbezahlbare Summer erwirbt, hängt sich Bond an seine Fersen an. Bonds Reise führt ihn zur geheimnisvollen Octopussy und schlussendlich auch wieder zurück nach Good-Old-Germany",
    'Filmnummer: 14  Jahr: 1985  Hauptdarsteller: Roger Moore  Deutscher Titel: Im Angesicht des Todes Originaltitel: A View To A Kill Inhalt: Als es Bond gelingt, einen Mikrochip aus Sibirien mitzubringen, stellt sich heraus, dass dieser sogar eine Atomexplosion überstehen würde. Warum? Dieser Sache soll 007 auf den Grund gehen, und seine Spur führt ihn zum Psychopaten und Millionär Max Zorin. Gemeinsam mit seinem alten Kollegen und Pferdeliebhaber „Tibbet" tarnt 007 als Adeliger und Chauffeur. Beide machen sich auf den Weg das Geheimnis zu lüften, warum Zorins Pferde bei jedem Rennen gewinnen. Es stellt sich heraus, dass diese alle einen Mikrochip implantiert haben. Bonds Reise führt ihn über Frankreich ins Silicon Valley und schlussendlich zur Golden Gate Bridge, wo es zum letzten Kampf zwischen Bond und Zorin kommt.',
    "Filmnummer: 15  Jahr: 1987  Hauptdarsteller: Timothy Dalton  Deutscher Titel: Der Hauch des Todes Originaltitel: The Living Daylights Inhalt: Bond wird nach Bratislava geschickt um den russischen Agenten Koskov per Pipeline nach Österreich überlaufen zu lassen. Da der russische Agent nur knapp einem Anschlag entgangen ist, fährt Bond noch einmal nach Bratislava zurück und lernt dort die wunderschöne Kara kennen, die der Sniperschütze war, der Koskov hätte töten sollen. Als sich herausstellt, dass das mögliche Attentat auf Koskov nur gestellt war, fliehen beide wieder zurück nach Österreich und schließlich über Wien nach Tanger. Dort stellt sich heraus, dass einige Drogen- und Waffenschmuggler hinter der gesamten Affäre um Koskov stecken.",
    "Filmnummer: 16  Jahr: 1989  Hauptdarsteller: Timothy Dalton  Deutscher Titel: Lizenz zum Töten Originaltitel: Licence To Kill Inhalt: Kurz vor der Hochzeit von Felix Leiter kommt die Meldung, das Drogenboss Sanchez per Flugzeug in der Nähe unterwegs sei. Diese Chance lassen sich die beiden, Bond und Leiter, nicht entgehen und fangen den Bösewicht. Dieser kommt aber einige Tage später wieder frei, tötet Leiters Frau und verletzt diesen selbst schwer! Was folgt ist ein beispielsloser Rachefeldzug vom verletzen und verärgerten James Bond… Nebenbei zerstört 007 noch Sanchez' riesiges Drogenlager und kann mit Hilfe einiger atemberaubenden LKW-Stunts Sanchez und dessen Handlanger schließlich zur Strecke bringen.",
    'Filmnummer: 17  Jahr: 1995  Hauptdarsteller: Pierce Brosnan  Deutscher Titel: GoldenEye Originaltitel: GoldenEye Inhalt: Der für tot gehaltene Ex-Kollege von James Bond, 006 Alec Trevelyan, „steht von den Toten auf" und versucht mit dem Super-Satelliten „Goldeneye", der alle elektronische Geräte in einem Umkreis von einigen Kilometern ausschalten kann, den größten Diebstahl aller Zeiten zu unternehmen.',
]

# --- Star Wars movies ---
docs_starwars = [
    "Filmnummer: 4  Jahr: 1977  Deutscher Titel: Krieg der Sterne  Originaltitel: Star Wars: Episode IV – A New Hope  Inhalt: In einer weit entfernten Galaxis kämpft die Rebellenallianz gegen das böse Galaktische Imperium. Die Prinzessin Leia wird vom Imperium gefangen genommen, nachdem sie die Pläne des Todessterns, einer riesigen Raumstation mit der Feuerkraft einer ganzen Flotte, an die Rebellen weitergeleitet hat. Der Farmerjunge Luke Skywalker findet durch den Droiden R2-D2 eine Nachricht von Leia und macht sich mit dem alten Jedi-Meister Obi-Wan Kenobi und dem Schmuggler Han Solo auf den Weg, sie zu befreien. Am Ende gelingt es Luke, den Todesstern mit einem gezielten Torpedoschuss in den Reaktorschacht zu zerstören.",
    "Filmnummer: 5  Jahr: 1980  Deutscher Titel: Das Imperium schlägt zurück  Originaltitel: Star Wars: Episode V – The Empire Strikes Back  Inhalt: Nach der Zerstörung des Todessterns verfolgt das Imperium die Rebellen auf den Eisplaneten Hoth und zwingt sie zur Flucht. Luke Skywalker begibt sich auf den Sumpfplaneten Dagobah, wo ihn der weise Jedi-Meister Yoda in der Macht ausbildet. Han Solo und Prinzessin Leia fliehen in die Wolkenstadt Bespin, geraten aber in eine Falle des skrupellosen Darth Vader. In einem dramatischen Duell verliert Luke seine Hand und erfährt, dass Darth Vader sein Vater ist.",
    "Filmnummer: 6  Jahr: 1983  Deutscher Titel: Die Rückkehr der Jedi-Ritter  Originaltitel: Star Wars: Episode VI – Return of the Jedi  Inhalt: Die Rebellen planen den Angriff auf einen zweiten, noch im Bau befindlichen Todesstern. Luke Skywalker stellt sich erneut Darth Vader und dem Imperator, um seinen Vater zur hellen Seite der Macht zurückzuführen. Auf dem Waldmond Endor kämpfen Han Solo und eine Gruppe Ewoks gegen die imperialen Streitkräfte. Anakin Skywalker wendet sich schließlich gegen den Imperator und rettet seinen Sohn, stirbt aber dabei. Das Imperium wird besiegt.",
    "Filmnummer: 1  Jahr: 1999  Deutscher Titel: Die dunkle Bedrohung  Originaltitel: Star Wars: Episode I – The Phantom Menace  Inhalt: Die Jedi-Ritter Qui-Gon Jinn und sein Padawan Obi-Wan Kenobi werden zur Handelsblockade des Planeten Naboo entsandt. Dort treffen sie auf Königin Amidala und den jungen Sklaven Anakin Skywalker, der eine außergewöhnliche Begabung in der Macht besitzt. Qui-Gon glaubt, dass Anakin der Auserwählte ist, der die Macht ins Gleichgewicht bringen soll. Im Hintergrund lauert der Sith-Lord Darth Maul, ein Schüler des geheimnisvollen Darth Sidious.",
    "Filmnummer: 2  Jahr: 2002  Deutscher Titel: Angriff der Klonkrieger  Originaltitel: Star Wars: Episode II – Attack of the Clones  Inhalt: Zehn Jahre nach den Ereignissen auf Naboo bedroht eine Separatistenbewegung die Republik. Obi-Wan Kenobi entdeckt auf dem Ozeanplaneten Kamino eine geheime Klonarmee, die für die Republik erschaffen wurde. Sein Schüler Anakin Skywalker begleitet Padmé Amidala zurück nach Naboo und verliebt sich in sie. Auf Tatooine sucht Anakin nach seiner von Tusken-Räubern entführten Mutter und tötet aus Wut alle Räuber. Die Klonkriege beginnen mit einer gewaltigen Schlachten auf dem Planeten Geonosis.",
    "Filmnummer: 3  Jahr: 2005  Deutscher Titel: Die Rache der Sith  Originaltitel: Star Wars: Episode III – Revenge of the Sith  Inhalt: Im letzten Jahr der Klonkriege wendet sich Anakin Skywalker langsam der dunklen Seite der Macht zu. Der skrupellose Kanzler Palpatine enthüllt sich als Darth Sidious und verführt Anakin mit dem Versprechen, das Leben von Padmé zu retten. Anakin wird zu Darth Vader und hilft, die Jedi-Ritter zu vernichten. Obi-Wan Kenobi besiegt den verletzten Vader auf dem Vulkanplaneten Mustafar. Das Galaktische Imperium wird ausgerufen und die Zwillinge Luke und Leia werden getrennt aufgezogen.",
    "Filmnummer: 7  Jahr: 2015  Deutscher Titel: Das Erwachen der Macht  Originaltitel: Star Wars: Episode VII – The Force Awakens  Inhalt: Dreißig Jahre nach dem Fall des Imperiums bedroht die neue Erste Ordnung unter Führung des maskierten Kylo Ren die Galaxis. Die junge Schrottsammlerin Rey auf dem Wüstenplaneten Jakku trifft auf den dessertierten Sturmtruppler Finn und den Droiden BB-8, der eine Karte zum verschollenen Luke Skywalker enthält. Han Solo und Chewbacca helfen Rey und Finn, die Resistenz zu erreichen. Kylo Ren tötet seinen eigenen Vater Han Solo. Rey entdeckt ihre Fähigkeiten in der Macht und besiegt Kylo Ren im Duell.",
    "Filmnummer: 8  Jahr: 2017  Deutscher Titel: Die letzten Jedi  Originaltitel: Star Wars: Episode VIII – The Last Jedi  Inhalt: Die Resistenz flieht vor der Flotte der Ersten Ordnung und sucht Verstärkung. Rey besucht Luke Skywalker auf der mystischen Insel Ahch-To und versucht ihn zu überzeugen, zurückzukehren. Luke ist desillusioniert und will den Jedi-Orden beenden. Rey und Kylo Ren entwickeln durch die Macht eine Verbindung zueinander. Yodas Geist erscheint Luke und gibt ihm neue Kraft. Luke opfert sich durch eine Macht-Projektion, um den Rückzug der Resistenz zu ermöglichen, und stirbt dabei.",
    "Filmnummer: 9  Jahr: 2019  Deutscher Titel: Der Aufstieg Skywalkers  Originaltitel: Star Wars: Episode IX – The Rise of Skywalker  Inhalt: Imperator Palpatine kehrt aus dem Nichts zurück und bedroht die Galaxis mit einer riesigen Flotte von Todesstern-Zerstörern. Rey erfährt, dass sie die Enkelin Palpatines ist. Gemeinsam mit Finn, Poe und ihren Freunden sucht sie nach einem Weg, Palpatines Flotte zu vernichten. Kylo Ren wendet sich zur hellen Seite zurück und wird wieder zu Ben Solo. Rey besiegt Palpatine mit der vereinten Kraft aller vergangenen Jedi-Meister, stirbt jedoch kurz danach, bevor Ben sie mit dem letzten Rest seiner Lebenskraft zurückbringt.",
]

store_bond = QdrantVectorStore.from_texts(
    docs_bond,
    embeddings,
    location=":memory:",
    collection_name="bond",
    force_recreate=True,
)

store_starwars = QdrantVectorStore.from_texts(
    docs_starwars,
    embeddings,
    location=":memory:",
    collection_name="starwars",
    force_recreate=True,
)

retriever_bond = store_bond.as_retriever(search_kwargs={"k": 3})
retriever_starwars = store_starwars.as_retriever(search_kwargs={"k": 3})

BOND_KEYWORDS = {"bond", "007", "james", "mi6", "geheimdienst", "spion", "agent"}
STARWARS_KEYWORDS = {
    "star",
    "wars",
    "jedi",
    "sith",
    "skywalker",
    "luke",
    "darth",
    "vader",
    "macht",
    "imperium",
    "galaxie",
    "galaxis",
    "yoda",
    "kenobi",
    "rey",
    "anakin",
}


class GraphState(TypedDict, total=False):
    question: str
    movie_type: Literal["bond", "starwars"]
    documents: list[Document]
    generation: str


def route(state: GraphState) -> Literal["retrieve_bond", "retrieve_starwars"]:
    question_lower = (state.get("question") or "").lower()
    words = set(question_lower.split())
    if words & STARWARS_KEYWORDS:
        return "retrieve_starwars"
    return "retrieve_bond"


def retrieve_bond(state: GraphState) -> GraphState:
    if "question" not in state:
        raise ValueError("question is required in state")

    question = state["question"]
    documents = retriever_bond.invoke(question)
    if not documents:
        documents = [Document(page_content="Keine Dokumente gefunden.")]

    print(f"-- [Bond] Retrieved {len(documents)} document(s) --")
    for i, doc in enumerate(documents):
        print(f"[{i + 1}] {doc.page_content[:120]}...")
    print()

    return {"movie_type": "bond", "documents": documents}


def retrieve_starwars(state: GraphState) -> GraphState:
    if "question" not in state:
        raise ValueError("question is required in state")

    question = state["question"]
    documents = retriever_starwars.invoke(question)
    if not documents:
        documents = [Document(page_content="Keine Dokumente gefunden.")]

    print(f"-- [Star Wars] Retrieved {len(documents)} document(s) --")
    for i, doc in enumerate(documents):
        print(f"[{i + 1}] {doc.page_content[:120]}...")
    print()

    return {"movie_type": "starwars", "documents": documents}


def generate(state: GraphState) -> GraphState:
    if "question" not in state or "documents" not in state:
        raise ValueError("question and documents are required in state")

    question = state["question"]
    documents = state["documents"]
    movie_type = state.get("movie_type", "bond")
    domain = "James-Bond-Filmen" if movie_type == "bond" else "Star-Wars-Filmen"

    prompt_template = """Du bist ein Assistent für Fragen zu {domain}.

# Anweisungen:
1. Beantworte die Frage ausschließlich anhand des gegebenen Kontexts.
2. Antworte auf Deutsch.
3. Sage "Diese Frage kann ich nicht beantworten.", wenn der Kontext nicht ausreicht.

# Kontext:
{{context}}

# Frage:
{{question}}
"""

    context = "\n\n".join(doc.page_content for doc in documents)
    prompt = prompt_template.format(domain=domain).format(
        context=context, question=question
    )
    generation = llm.invoke([HumanMessage(content=prompt)])
    return {"generation": cast(str, generation.content)}


workflow = StateGraph(GraphState)

workflow.add_node(retrieve_bond)
workflow.add_node(retrieve_starwars)
workflow.add_node(generate)

workflow.add_conditional_edges(START, route)
workflow.add_edge("retrieve_bond", "generate")
workflow.add_edge("retrieve_starwars", "generate")
workflow.set_finish_point("generate")

graph = workflow.compile()

png = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png)

query = "Welcher James-Bond-Film handelt vom russischen Konsulat in Istanbul?"
# query = "Auf welchem Planeten bildet Yoda Luke Skywalker in der Macht aus?"

langfuse_handler = CallbackHandler()

with langfuse.start_as_current_observation(name="simple-rag-langgraph") as span:
    span.update(input=query)

    print("-- Frage --")
    print(query)
    print()

    result = graph.invoke(
        {"question": query},
        config={"callbacks": [langfuse_handler]},
    )

    print("-- Antwort --")
    print(result["generation"])
    print()

    span.update(output=result["generation"])

    print(f"-- Trace ID: {span.trace_id} --")
    feedback = input("Feedback: ").strip()
    if feedback:
        langfuse.create_score(
            trace_id=span.trace_id,
            name="user-feedback",
            value=feedback,
        )
    print("Feedback gespeichert")

langfuse.flush()
