from utils import delete, get, post, put


class ObjectIsDeletedError(Exception):
    pass


class BaseData:
    _create_data = dict(json_page="", action="")
    _delete_data = dict(json_page="", action="")
    _get_data = dict(json_page="", action="")
    _list_data = dict(json_page="", action="")
    _update_data = dict(json_page="", action="")
    _required_properties = []
    _auto_data = []
    _assigning_data = False
    _is_deleted = False


    @classmethod
    def create(cls, **kwargs):
        nothing = object()
        for argument in cls._required_properties:
            if kwargs.get(argument, nothing) == nothing:
                raise ValueError('"{}" is required to create this object'.format(argument))

        kwargs.update(cls._create_data)
        element_data = post(**kwargs)
        element = cls()
        element._set_data(**element_data)
        return element

    def delete(self):
        if self._is_deleted:
            raise ObjectIsDeletedError("This object doesn't exist anymore")

        kwargs = dict(instance_id=self.id)
        kwargs.update(self._delete_data)
        delete(**kwargs)
        self._is_deleted = True

    @classmethod
    def get(cls, instance_id):
        kwargs = dict(instance_id=instance_id)
        kwargs.update(cls._get_data)
        element_data = get(**kwargs)
        element = cls()
        element._set_data(id=instance_id)
        element._set_data(**element_data)
        return element

    @classmethod
    def list(cls):
        elements = get(**cls._list_data)
        instances = []
        for element in elements:
            instance = cls()
            instance._set_data(**element)
            instances.append(instance)

        return instances

    def update(self):
        if self._is_deleted:
            raise ObjectIsDeletedError("This object doesn't exist anymore")

        kwargs = self._update_data
        for prop in vars(self.__class__):
            if callable(getattr(self.__class__, prop)):
                continue

            if prop.startswith('_'):
                continue

            val = getattr(self, prop)
            if val is None:
                continue

            if prop not in self._auto_data:
                kwargs[prop] = getattr(self, prop)

        element_data = put(instance_id=self.id, **kwargs)
        self._set_data(**element_data)
        return self

    def _set_data(self, **data):
        """
        This method assigns every keyword argument to its equivalent property. If the property doesn't exist, it is 
        discarded.
        :param data: some keyword arguments
        """
        tmp = self._assigning_data
        self._assigning_data = True
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self._assigning_data = tmp

    def __setattr__(self, key, value):
        if self._is_deleted:
            raise ObjectIsDeletedError("This object doesn't exist anymore")

        if not self._assigning_data:
            if key in self._auto_data:
                raise Exception("The following properties are set automatically and can't be edited : {}".format(
                    self._auto_data))

        super().__setattr__(key, value)

    def is_deleted(self):
        return self._is_deleted


# Values for the fields

class DocumentKind:
    bill = "vat"  # pour facture
    estimate = "estimate"  # pour devis      
    proforma = "proforma"  # Facture proforma
    correction = "correction"  # pour avoir
    order = "client_order"  # pour bon de commande de client
    receipt = "receipt"  # pour reçu
    advance = "advance"  # pour facture d'acompte
    final = "final"  # pour facture de solde
    other = "invoice_other"  # pour autre type de document
    kp = "kp"  # pour bon d'entrée de caisse
    kw = "kw"  # pour bon de sortie de caisse
    

class DocumentIncome:
    income = 1  # Revenu
    expense = 0  # Dépense


class CalculatingStrategy:
    position = "default"  # "default" ou "keep_gross"  # Comment se calcule le total de chaque ligne
    sum = "sum"  # ""sum" ou "keep_gross" ou "keep_net"  # Comment se calcule le total des colonnes
    invoice_form_price_kind = "net"  # "net" ou "gross"  # prix unitaire (HT ou TTC)


class PaymmentType:
    transfer = "transfer"  # virement bancaire
    card = "card"  # carte bancaire
    cash = "cash"  # espèce
    cheque = "cheque"  # chèque
    paypal = "paypal"  # PayPal
    off = "off"  # aucun(ne pas afficher)
    any_other_text_entry = "any_other_text_entry"  # autre


class Status:
    issued = "issued"  # Créé
    sent = "sent"  # Envoyé
    paid = "paid"  # Payé
    partial = "partial"  # Payé en partie
    rejected = "rejected"  # Refusé
    accepted = "accepted"  # Accepté


# Models


# @todo Test this
class Seller(BaseData):
    seller_name = "Ma Société"  # Nom du département vendeur. Si ce champ n'est pas renseigné, le département principal est sélectionné par défaut. Préférez plutôt "department_id". Si vous utilisez toutefois "seller_name", le système tentera d'identifier le département portant ce nom, sinon il créera un nouveau département.
    seller_tax_no = "FR5252445767"  # numéro d'identification fiscale du vendeur (ex: n° TVA)
    seller_bank_account = "24 1140 1977 0000 5921 7200 1001"  # coordonnées bancaires du vendeur
    seller_bank = "CREDIT AGRICOLE"  # domiciliation bancaire
    seller_post_code = "75007"  # code postal du vendeur
    seller_city = "Paris"  # ville du vendeur
    seller_street = "21 Rue des Mimosas"  # numéro et nom de rue du vendeur
    seller_country = ""  # pays du vendeur
    seller_email = "contact@chose.com"  # email du vendeur
    seller_www = ""  # site internet du vendeur
    seller_fax = ""  # numéro de fax du vendeur
    seller_phone = ""  # numéro de tel du vendeur
    seller_person = ""  # Nom du vendeur (figurant en bas de page des documents)
    department_id = "1"  # ID du département vendeur (depuis Paramètres > Compagnies/Départments, cliquer sur le nom de la compagnie/département pour visualiser l'ID dans l'url affiché). Le système affichera alors automatiquement les coordonnées du département vendeur (nom, adresse...) sur le document (les autres champs "seller_" ne sont plus nécessaires).


class Client(BaseData):
    _create_data = dict(json_page="clients", action="client")
    _delete_data = dict(json_page="clients", action="client")
    _get_data = dict(json_page="clients", action="client")
    _list_data = dict(json_page="clients", action="clients")
    _update_data = dict(json_page="clients", action="client")
    _required_properties = ['name']
    _auto_data = ['created_at', 'updated_at', 'shortcut', 'deleted']

    id = None
    buyer_id = None
    name = None
    first_name = None
    last_name = None
    company = None
    title = None
    department_id = None
    category_id = None
    shortcut = None

    tax_no = None
    street_no = None
    street = None
    post_code = None
    city = None
    country = None
    email = None
    phone = None
    mobile_phone = None
    www = None
    fax = None

    bank = None
    bank_account = None
    payment_to_kind = None
    bank_account_id = None
    tax_no_check = None
    default_payment_type = None
    tax_no_kind = None
    accounting_id = None

    deleted = None
    created_at = None
    updated_at = None

    note = None

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


# @todo Test this
class Product(BaseData):
    _create_data = dict(json_page="products", action="product")
    _delete_data = dict(json_page="products", action="product")
    _get_data = dict(json_page="products", action="product")
    _list_data = dict(json_page="products", action="products")
    _update_data = dict(json_page="products", action="product")
    _required_properties = []

    id = None
    name = None
    code = None
    additional_info = None
    price_net = None
    tax = None


# @todo Test this
class Document(BaseData):
    number = None  # "13/2012" - numéro du document (généré automatiquement si non indiqué)
    kind = DocumentKind.bill
    income = DocumentIncome.income
    issue_date = None  # "2013-01-16" - date de création
    place = "Paris"  # lieu de création
    sell_date = "off"   # - date additionnelle (ex: date de vente) : date complète ou juste mois et année:YYYY-MM. Pour ne pas faire apparaître cette date, indiquez "off" (ou décochez l'option "Afficher la Date additionnelle" depuis vos paramètres du compte).
    category_id = ""  # ID de la catégorie
    seller = None
    buyer = None
    additional_info = "0"  # afficher (1) ou non (0) la colonne aditionnelle
    additional_info_desc = "Origine"  # titre de la colonne aditionnelle
    show_discount = "0"  # afficher (1) ou non (0) la colonne réduction
    payment_type = PaymmentType.transfer  # mode de règlement
    payment_to_kind = 31  # date limite de règlement (parmi les options proposées). Si l'option est "Autre" ("other_date"), vous pouvez définir une date spécifique grâce au champ "payment_to". Si vous indiquez "5", la date d'échéance est de 5 jours. Pour ne pas afficher ce champ, indiquez "off".
    payment_to = "2013-01-16"  # date limite de règlement
    status = Status.issued  # état du document
    paid = "0,00"  # montant payé
    oid = "10021"  # numéro de commande (ex: numéro généré par une application externe)
    oid_unique = "yes"  # si la valeur est «yes», alors il ne sera pas permis au système de créer 2 factures avec le même OID (cela peut être utile en cas de synchronisation avec une boutique en ligne)
    warehouse_id = "1090"  # numéro d'identification de l'entrepôt
    description = ""  # Informations spécifiques
    paid_date = ""  # Date du paiement
    currency = "EUR"  # devise
    lang = "fr"  # langue du document
    exchange_currency = ""  # convertir en (la conversion du montant total et du montant de la taxe en une autre devise selon taux de change du jour)
    title = ""  # Objet
    internal_note = ""  # Notes privées
    invoice_template_id = "1"  # format d'impression
    description_footer = ""  # Bas de page
    description_long = ""  # Texte additionnel (imprimé sur la page suivante)
    from_invoice_id = ""  # ID du document de référence depuis lequel le document a été généré (utile par ex quand une facture est générée depuis un devis)
    positions = []  # Liste de positions
    hide_tax = "1"  # Montant TTC uniquement (ne pas afficher de montant HT ni de taxe)
    calculating_strategy = CalculatingStrategy()

    def add_position(self, product, quantity):
        position = Position()
        position.product = product
        position.quantity = quantity
        self.positions.append(position)

    def __init__(self, doc_id=None, seller: Seller = None, buyer: Client = None):
        self.oid = doc_id
        self.seller = seller
        self.buyer = buyer


# @todo Test this
class Position(BaseData):
    product: None
    discount_percent = ""  # % de la réduction (remarque: afin de pouvoir appliquer la réduction, il faut au préalable donner à "show_discount" la valeur de 1 et vérfier si dans les Paramètres du compte > Options par défaut, l'option choisie sous le champ 'Comment calculer la réduction' est 'pourcentage du prix unitaire net')
    discount = "",  # montant de la réduction (remarque: afin de pouvoir appliquer la réduction, il faut au préalable donner à "show_discount" la valeur de 1 et vérfier si dans les Paramètres du compte > Options par défaut, l'option choisie sous le champ 'Comment calculer la réduction' est 'Montant (TTC)')
    quantity = "1"  # quantité
    quantity_unit = "kg"  # unité
    price_gross = "72,57"  # prix unitaire TTC (calculé automatiquement si non indiqué)
    total_price_net = "59,00"  # total HT (calculé automatiquement si non indiqué)
    total_price_gross = "72,57"  # total TTC

