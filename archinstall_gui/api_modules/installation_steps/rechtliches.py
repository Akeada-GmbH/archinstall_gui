import json
import urllib.request
from os import walk
from os.path import isdir, isfile, abspath
from time import time

html = """
<div class="padded_content flex_grow flex column" style="min-width:100%;">
    <h3><b>NUTZUNGS- & LIZENZBEDINGUNGEN</b></h3>
    
    <span>
    BITTE LESEN SIE SICH DIE NUTZUNGSBEDINGUNGEN AUFMERKSAM DURCH. BESTÄTIGEN SIE DIE ZURKENNTNISSNAHME UND STIMMEN SIE EBENFALLS DEN LIZENZBEDINGUNGEN ZU.
    </span>

    <div style="padding-top:50px;">
        <div style="background-color:#ffff88;border:1px solid #ccc;overflow:auto;max-height:150px;">
        <font face="Calibri Light, serif"><font size="2" style="font-size: 8pt"><u><b>HAFTUNGSAUSSCHLUSS</b></u></font></font></p>
            <p style="line-height: 106%; margin-bottom: 0.28cm"><font size="4" style="font-size: 8pt"><b>WICHTIG:&nbsp;NUTZEN
            SIE DEN PRIVASTICK NICHT AUF GERÄTEN, AUF DENEN SIE UNGESICHERTE
            DATEN HABEN ODER WELCHE FÜR WICHTIGE INFRASTRUKTUREN ZUSTÄNDIG
            SIND. NUTZEN SIE DEN PRIVASTICK NUR AUF GERÄTEN, BEI DEREN
            FEHLFUNKTION KEIN SCHADEN AN DRITTEN ENSTEHT ODER WICHTIGE,
            UNGESICHERTE DATEN VERLOREN GEHEN KÖNNTEN. HABEN SIE IMMER EIN
            BACKUP IHRER WICHTIGEN DATEN. </b></font>
            </p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Es besteht
            keinerlei Gewährleistung für das Programm, soweit dies gesetzlich
            zulässig ist. Sofern nicht anderweitig schriftlich bestätigt,
            stellen die Urheberrechtsinhaber und/oder Dritte das Programm so zur
            Verfügung, „wie es ist“, ohne irgendeine Gewährleistung, weder
            ausdrücklich noch implizit, einschließlich – aber nicht begrenzt
            auf – die implizite Gewährleistung der Marktreife oder der
            Verwendbarkeit für einen bestimmten Zweck. Das volle Risiko
            bezüglich Qualität und Leistungsfähigkeit des Programms liegt bei
            Ihnen. Sollte sich das Programm als fehlerhaft herausstellen, liegen
            die Kosten für notwendigen Service, Reparatur oder Korrektur bei
            Ihnen.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm"><font size="2" style="font-size: 8pt"><b>HAFTUNGSBEGRENZUNG</b></font></p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">In keinem Fall,
            außer wenn durch geltendes Recht gefordert oder schriftlich
            zugesichert, ist irgendein Urheberrechtsinhaber oder irgendein
            Dritter, der das Programm wie oben erlaubt modifiziert oder
            übertragen hat, Ihnen gegenüber für irgendwelche Schäden haftbar,
            einschließlich jeglicher allgemeiner oder spezieller Schäden,
            Schäden durch Seiteneffekte (Nebenwirkungen) oder Folgeschäden, die
            aus der Benutzung des Programms oder der Unbenutzbarkeit des
            Programms folgen (einschließlich – aber nicht beschränkt auf –
            Datenverluste, fehlerhafte Verarbeitung von Daten, Verluste, die von
            Ihnen oder anderen getragen werden müssen, oder dem Unvermögen des
            Programms, mit irgendeinem anderen Programm zusammenzuarbeiten),
            selbst wenn ein Urheberrechtsinhaber oder Dritter über die
            Möglichkeit solcher Schäden unterrichtet worden war.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm"><font size="3" style="font-size: 8pt"><b>Sonstiges</b></font></p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Für Mängel der
            Software haftet der Anbieter nach Maßgabe der gesetzlichen
            Bestimmungen des Kaufrechts (§§ 434 ff. BGB).</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Bei leichter
            Fahrlässigkeit haftet der Anbieter nur bei Verletzung
            vertragswesentlicher Pflichten (Kardinalpflichten) sowie bei
            Personenschäden nach Maßgabe des</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Produkthaftungsgesetzes.
            Im Übrigen ist die vorvertragliche, vertragliche und
            außervertragliche Haftung des Anbieters auf Vorsatz und grobe
            Fahrlässigkeit beschränkt, wobei die Haftungsbegrenzung auch im
            Falle des Verschuldens eines Erfüllungsgehilfen des Anbieters gilt.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Die Software,
            Hardware und Ihre Dokumentation wird &quot;wie sie ist&quot; und ohne
            jede Gewährleistung für Funktion, Korrektheit oder Fehlerfreiheit
            zur Verfügung gestellt.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Für jedweden
            direkten oder indirekten Schaden - insbesondere Schaden an anderer
            Software, Schaden an Hardware, Schaden durch Nutzungsausfall und
            Schaden durch Funktionsuntüchtigkeit der Software, kann der Autor
            nicht haftbar gemacht werden. Ausschließlich der Benutzer haftet für
            die Folgen der Benutzung dieser Software.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Diese Software
            wurde mit größter Sorgfalt entwickelt, jedoch können Fehler
            niemals ausgeschlossen werden. Es kann daher keine Gewähr für die
            Sicherheit Ihrer Daten übernommen werden.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Sollte die
            gelieferte Sache einschließlich der Handbücher und sonstiger
            Unterlagen Mängel aufweisen, so werden diese vom Lieferanten
            innerhalb der gesetzlich vorgeschriebenen Frist von zwei Jahren ab
            Ablieferung - nach entsprechender Mitteilung durch den Anwender -
            behoben. Hierbei hat der Kunde die Wahl zwischen einer kostenfreien
            Nachbesserung oder Ersatzlieferung. Eine Ersatzlieferung erfolgt nur
            gegen Rückgewähr der mangelhaften Sache.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Dem Kunden steht
            nach seiner Wahl das Verlangen nach einer Herabsetzung der Vergütung
            (Minderung) oder der Rücktritt vom Vertrag zu, soweit der Mangel
            nicht innerhalb angemessener Frist behoben werden kann, das Gesetz
            eine Fristsetzung als entbehrlich erachtet oder die Nachbesserung/
            Ersatzlieferung aus sonstigen Gründen als fehlgeschlagen anzusehen
            ist. Ein Fehlschlagen der Nachbesserung ist erst gegeben, wenn dem
            Verkäufer hinreichende Gelegenheit zur Nachbesserung oder
            Ersatzlieferung eingeräumt wurde, ohne dass der gewünschte Erfolg
            erzielt wurde, was in der Regel erst nach zwei Fehlversuchen gegeben
            ist. Außerdem ist ein Fehlschlagen gegeben, wenn Nachbesserung oder
            Ersatzlieferung vom Verkäufer verweigert oder unzumutbar verzögert
            wird. Ferner wenn begründete Zweifel hinsichtlich der
            Erfolgsaussichten bestehen oder wenn eine Unzumutbarkeit aus
            sonstigen Gründen vorliegt.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Den Kunden trifft
            eine Untersuchungs- und Rügeobliegenheit. Ein Kunde ist daher
            verpflichtet, die gelieferte Ware auf offensichtliche Mängel, die
            einem durchschnittlichen Kunden ohne weiteres auffallen, zu
            untersuchen. Zu den offensichtlichen Mängeln zählen insbesondere
            das Fehlen von Handbüchern sowie erhebliche, leicht sichtbare
            Beschädigungen der Ware. Sollte eine andere Sache oder eine zu
            geringe Menge geliefert werden, handelt es sich auch hierbei um einen
            offensichtlichen Mangel. Solche offensichtlichen Mängel sind
            innerhalb von vier Wochen nach Lieferung beim Verkäufer schriftlich
            zu rügen. Mängel, die erst später offensichtlich werden, müssen
            innerhalb von vier Wochen nach dem Erkennen durch den Kunden beim
            Verkäufer gerügt werden. Sollte der Kunde seiner Untersuchungs- und
            Rügeobliegenheit nicht nachkommen, gilt die Ware in Ansehung des
            betreffenden Mangels als genehmigt.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Sollte eine
            Bestimmung des Vertrages unwirksam sein, so werden dadurch die
            übrigen Bestimmungen in ihrer rechtlichen Wirksamkeit nicht berührt.
            An die Stelle der unwirksamen Bestimmung soll für diesen Fall mit
            anfänglicher Wirkung eine solche treten, die dem beabsichtigten Sinn
            und Zweck der Parteien entspricht und ihrem Inhalt nach durchführbar
            ist.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Bei
            Rechtsstreitigkeiten aus diesem Vertrag ist der Sitz des Verkäufers
            Gerichtsstand, wenn der Kunde Kaufmann ist oder er keinen allgemeinen
            Gerichtsstand im Gebiet der Bundesrepublik Deutschland hat oder
            juristische Person des öffentlichen Rechts ist.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Der Verkäufer
            ist berechtigt, auch an jedem anderen gesetzlich vorgesehenen
            Gerichtsstand zu klagen.</p>
            <p style="line-height: 106%; margin-bottom: 0.28cm">Für diesen
            Vertrag gilt das Recht der Bundesrepublik Deutschland unter
            Ausschluss des UN-Kaufrechts.</p>
        </div>
        
    </div>
    <span style="padding-top:5px;">
        Ich habe den Haftungsschluss des PrivaStick gelesen und akzeptiere ausdrücklich. <input type="checkbox" id="checkbox1" value="no" onclick="validate(this)"/>
    </span>

    <div style="padding-top:50px;">
        <div style="background-color:#ffff88;border:1px solid #ccc;overflow:auto;max-height:150px;">
        <font face="Calibri Light, serif"><font size="2" style="font-size: 8pt"><u><b>Software-Nutzungsbestimmungen</b></u></font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="2" style="font-size: 8pt">Diese
            Software-Nutzungsbestimmungen gelten für sämtliche Angebote, das
            heißt alle in Bezug auf Software oder Hardware angebotene
            Leistungen, von PrivaStick vertreten durch Akeada GmbH (folgend
            PrivaStick genannt).</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Indem
            Sie diese Software-Nutzungsbestimmungen („Nutzungsbestimmungen“)
            bei Vertragsabschluss oder während des Installations-,
            Registrierungs- oder Anmeldevorgangs annehmen oder indem Sie auf
            unsere Angebote zugreifen oder diese nutzen, bestätigen Sie, dass
            Sie diese Nutzungsbestimmungen annehmen. Ohne die erforderliche
            Zustimmung sind Sie nicht berechtigt, den PrivaStick zu nutzen.</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Sie
            stimmen diesen Nutzungsbestimmungen im Namen der Gesellschaft oder
            juristischen Person zu, in deren Auftrag Sie handeln (z. B. als
            Mitarbeiter oder Auftragnehmer), oder, sofern eine entsprechende
            Gesellschaft oder juristische Person nicht existiert, in Ihrem
            eigenen Namen als natürliche Person (jeweils „Sie“). Sie sichern
            zu und gewährleisten, dass Sie berechtigt und befugt sind, im Namen
            der juristischen Person (sofern existent) und im eigenen Namen zu
            handeln und diese juristische Person bzw. sich selbst zu binden.</font></font></p>
            <h1 class="western"><b>Software</b></h1>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Software
            bezeichnet Software oder ähnliche Materialien, insbesondere auch
            Module, Komponenten, Leistungsmerkmale und Funktionen, die von
            PrivaStick zur Verfügung gestellt werden, gleich, ob sie im Rahmen
            eines Abonnements und ob sie gegen Entgelt zur Verfügung gestellt
            werden oder nicht. Software schließt Updates und Upgrades ein.</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Bei
            Angeboten, die aus Software bestehen, die PrivaStick Ihnen
            bereitstellt oder liefert, und vorbehaltlich der Einhaltung dieser
            Nutzungsbestimmungen sowie sämtlicher Zahlungsverpflichtungen, räumt
            Ihnen PrivaStick für die Lizenzlaufzeit eine nicht exklusive, nicht
            unterlizenzierbare, Lizenz zur Installation und Nutzung der Software
            ein; die Installation und Nutzung darf ausschließlich (i) gemäß
            der Dokumentation für das Angebot und (ii) im Rahmen Ihres
            Abonnements / Kaufs, einschließlich der gestatteten Anzahl,
            Lizenzart, des Gebiets sowie anderer für die Art, die Sie beim
            Abonnieren des Angebots ausgewählt haben, festgelegten Attribute,
            erfolgen.&nbsp;Mitgelieferte und zu Bestätigende
            Lizenzvereinbarungen sind ebenfalls zu beachten.</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Während
            der Laufzeit Ihres Abonnements kann PrivaStick Ihnen Updates oder
            Upgrades der Software zugänglich machen oder bereitstellen. Für
            diese Updates und Upgrades gelten die gleichen Lizenz- Haftungs- und
            anderen Bedingungen wie für die Software, auf die sich die Updates
            oder Upgrades beziehen. Wir empfehlen Ihnen, sämtliche Ihnen während
            der Laufzeit Ihres Abonnements zugänglich gemachten Updates und
            Upgrades unverzüglich zu installieren und zu nutzen.&nbsp;</font></font></p>
            <h1 class="western"><b>Zugriff auf und Nutzung von Angeboten</b></h1>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Je
            nach Angebot müssen Sie sich ggf. in Ihr Konto einloggen, um das
            Angebot zu aktivieren, (weiterhin) zu nutzen oder (weiterhin) darauf
            zuzugreifen. Nur Sie einschließlich Ihrer Autorisierten Benutzer
            dürfen ein Angebot nutzen oder darauf zugreifen. Der Zugriff auf und
            die Nutzung alle(r) Angebote hängt (unter anderem) von Ihrer
            rechtzeitigen Zahlung aller maßgeblichen Beträge für die Angebote,
            einschließlich Steuern und anderer Entgelte, sowie der Einhaltung
            dieser Nutzungsbestimmungen ab.</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Manche
            Angebote veranlassen Ihre elektronischen Geräte ggf. dazu, sich
            automatisch mit dem Internet zu verbinden (sporadisch oder
            regelmäßig) - beispielsweise, um Ihr Abonnement auf Gültigkeit zu
            überprüfen, Ihnen Zugriff auf Dienste zu gewähren (einschließlich
            Diensten von Drittanbietern) oder Updates oder Upgrades
            herunterzuladen und zu installieren; dies geschieht möglicherweise
            ohne weitere Mitteilung an Sie. Sie stimmen einer solchen Verbindung
            und Überprüfung Ihres Abonnements auf Gültigkeit sowie dem
            automatischen Herunterladen und Installieren von Updates und Upgrades
            zu.&nbsp;</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Die
            Angebote schließen keinen Zugang zum Internet oder zu anderen
            Netzwerken oder Kommunikationsdiensten und keine Hardware-,
            Software-, Speicher-, Sicherheits- oder sonstigen Ressourcen ein, die
            für den Zugriff auf oder die Nutzung der Angebote erforderlich sind.
            Sie und Ihre anderen Anbieter und Dienstleister sind für den Erwerb
            all dieser Elemente und für ihre Verlässlichkeit, Sicherheit und
            Leistung verantwortlich.</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Nicht
            alle Angebote und nicht alle Funktionen eines Angebots sind an allen
            Orten und in allen Sprachen verfügbar.&nbsp;</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt"><font color="#2f5496"><font face="Calibri Light, serif"><font size="4" style="font-size: 16pt"><b>Nutzungsbeschränkung,
            Datensicherheit</b></font></font></font><br/>
            <br/>
            Bei den Angeboten
            handelt es sich um Software, die dazu bestimmt sind, Ihre
            Onlineaktivitäten zu verschlüsseln (mittels VPN und/oder
            softwareseitiger Einstellungen)</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">PrivaStick
            ist in keiner Weise für die anhand der Nutzung der Angebote erzielte
            Sicherheit oder Anonymität verantwortlich.</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Ihre
            Verantwortung umfasst ohne Einschränkung die Festlegung angemessener
            Nutzungen der Angebote und die Auswahl der Angebote und anderer
            Computerprogramme und Materialien, die Sie bei der Erzielung der von
            Ihnen beabsichtigten Ergebnisse unterstützen sollen. Sie sind ferner
            für die Beurteilung der Eignung unabhängiger Verfahren zur Prüfung
            der Verlässlichkeit, Genauigkeit, Vollständigkeit, Kompatibilität
            mit anwendbaren rechtlichen Anforderungen und sonstiger Eigenschaften
            von Ausgaben verantwortlich, einschließlich insbesondere aller mit
            Unterstützung des PrivaStick genutzten Onlinedienste, Angebote oder
            ähnlichem.</font></font></p>
            <h1 class="western"><b>Zulässige Nutzung des PrivaSTick</b></h1>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Sie
            greifen auf Angebote zu und nutzen diese (und genehmigen deren
            Nutzung und den Zugriff darauf) nur im Einklang mit allen anwendbaren
            Gesetzen (und werden diese einhalten). </font></font>
            </p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Sie
            dürfen den PrivaStick nicht nutzen, wenn Sie während der Nutzung:</font></font></p>
            <ul>
                <li><p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0cm">
                <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Gegen
                geltendes Rechtverstoßen.</font></font></p>
                <li><p style="line-height: 100%; margin-bottom: 0cm"><font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Bewusst
                oder unbewusst Straftaten begehen</font></font></p>
                <li><p style="line-height: 100%; margin-bottom: 0.49cm"><font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Die
                Anonymisierungsmechanismen des PrivaStick dafür nutzen,
                strafrechtlich relevanten taten zu verschleiern.</font></font></p>
            </ul>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            •&nbsp;&nbsp; &nbsp;<font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Angebote
            im oder über das Internet (außer im Falle der Bereitstellung durch
            PrivaStick über das Internet), in Wide-Area-Netzwerken (WANs) oder
            anderen nicht lokalen Netzwerken; oder
            Anwendungsvirtualisierungtechnologien, Web-Hosting, Timesharing,
            Software as a Service, Platform as a Service, Infrastructure as a
            Service, Cloud- oder andere Web-basierte, gehostete oder ähnliche
            Dienste nutzen oder in dieser Weise darauf zugreifen;&nbsp;</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            •&nbsp;&nbsp; &nbsp;<font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Hinweise
            zu Urheberrechten, Marken, Vertraulichkeit oder anderen
            Eigentumsrechten von Angeboten, Dokumentation oder dazugehörigem
            Material entfernen; und</font></font></p>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            •&nbsp;&nbsp; &nbsp;<font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">die
            Leistungsfähigkeit von technischen Sicherheitsvorkehrungen aufheben,
            deaktivieren oder anderweitig einschränken, die PrivaStick dazu
            verwendet, (i) die Installation und Nutzung der sowie den Zugriff auf
            die Angebote zu verwalten, überwachen, kontrollieren oder
            analysieren, oder (ii) die gewerblichen Schutzrechte von PrivaStick
            zu schützen;&nbsp;</font></font></p>
            <h1 class="western"><b>Datensicherung</b></h1>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">PrivaStick
            empfiehlt, dass Sie Ihren Inhalt sichern und schützen, indem Sie
            geeignete Verschlüsselungs- und Sicherheitstechnologien einsetzen.
            Sie erkennen an, dass Online-Dienste von gelegentlichen
            Unterbrechungen oder Ausfällen betroffen sein können, und dass Sie
            infolgedessen ggf. nicht in der Lage sind, Ihren Inhalt abzurufen.
            PrivaStick empfiehlt, dass Sie regelmäßig ein Backup von Ihrem
            Inhalt erstellen und speichern. Sie sind jederzeit für die
            Aufbewahrung und fortlaufende Erstellung solcher Backup-Kopien Ihres
            Inhalts verantwortlich.</font></font></p>
            <h1 class="western"><b>Verschwiegenheitsvereinbarung</b></h1>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Vertrauliche
            Informationen bezeichnet der Öffentlichkeit nicht allgemein bekannte
            Informationen, die (i) eine Offenlegende Partei einer Empfangenden
            Partei schriftlich zur Verfügung stellt oder offenlegt, und (ii) von
            der Offenlegenden Partei schriftlich als vertraulich bezeichnet
            werden. PrivaStick Vertrauliche Informationen umfassen auch die nicht
            öffentlichen Aspekte von (i) Angeboten und damit verbundenen
            Produktplänen, Technologien und sonstigen technischen Informationen.</font></font></p>
            <h1 class="western"><b>Freistellung</b></h1>
            <p style="line-height: 100%; margin-top: 0.49cm; margin-bottom: 0.49cm">
            <font face="Times New Roman, serif"><font size="3" style="font-size: 8pt">Sie
            werden PrivaStick von sämtlichen Verlusten, Haftungsansprüchen,
            Kosten (einschließlich angemessener Anwaltsgebühren) freistellen
            (und auf Verlangen von PrivaStick dagegen verteidigen), die
            PrivaStick aufgrund von Forderungen, Klagen oder Verfahren
            („Forderung“) entstehen im Zusammenhang mit (i) Ihrem Inhalt,
            (ii) Ihrer Nutzung (einschließlich der Ihrer Autorisierten Benutzer)
            von Angeboten, einschließlich der Ausgabe oder anderer, durch eine
            solche Nutzung generierter Ergebnisse, und (iii) Ihrer Verletzung
            (einschließlich der Ihrer Autorisierten Benutzer) dieser
            Nutzungsbestimmungen, einschließlich einer Forderung, die geltend
        macht oder vorgibt, auf Fahrlässigkeit von PrivaStick zu beruhen.</font></font></p>
        </div>
    </div>
    <span style="padding-top:5px;">
        Ich habe den Software-Nutzungsbedingungen des PrivaStick gelesen und akzeptiere sie ausdrücklich. <input type="checkbox" id="checkbox2" value="no" onclick="validate(this)"/>
    </span>


</div>

<div class="form-group" style="padding-left:10px; padding-right:10px;">
    <button id="back_step" class="btn btn-primary btn-lg"
            type="submit">
         Zurück
    </button>
    <button id="skip_step" class="btn btn-secondary btn-lg float-right no-click"
            type="submit">
         Weiter
    </button>
</div>

"""

## TODO:
## Needs to be loaded this way, since we can't inject JS into divs etc in the HTML above.
javascript = """
function validate(checkbox) {
  var c1 = document.getElementById("check1");
  var c2  = document.getElementById("check2");
    console.log("test")
  if (checkbox1.checked && checkbox2.checked) {
    // alert("checked");

        var continue_button = document.getElementById("skip_step");
        continue_button.classList.remove("no-click");
        continue_button.classList.remove("btn-secondary");
        continue_button.classList.add("btn-primary");

  } else {
    // alert("You didn't check it all!");
  }
}

document.querySelector('#back_step').addEventListener('click', function() {
    socket.send({
        '_module' : 'installation_steps/willkommen',
        'back' : true
    })
})


window.checkInternetConnection = () => {
    var isOnLine = navigator.onLine;
    console.log('Initially ' + (window.navigator.onLine ? 'on' : 'off') + 'line');
    if (isOnLine) {
        document.querySelector('#skip_step').addEventListener('click', function() {
            socket.send({
                '_module' : 'installation_steps/internet',
                'skip' : true,
                'dependencies' : ['vpn']
            })
        })
    } else {
        document.querySelector('#skip_step').addEventListener('click', function() {
            socket.send({
                '_module' : 'installation_steps/internet',
            })
        })
    }

}

window.onload = window.checkInternetConnection();

"""

def on_request(frame):
    if '_module' in frame.data and frame.data['_module'] == 'installation_steps/rechtliches':
        if 'back' in frame.data:
            yield {
                'status' : 'success',
                '_modules' : 'vpn'
            }
            yield {
                'status' : 'success',
                '_modules' : 'internet'
            }
            yield {
                'status' : 'success',
                '_modules' : 'rechtliches'
            }
            yield {
                'next' : 'rechtliches',
                'status' : 'success',
                '_modules' : 'internet'
            }
        yield {
            '_modules' : 'willkommen',
            'status' : 'complete',
        }
        yield {
            'html' : html,
            'javascript' : javascript,
            '_modules' : 'vpn'
        }
