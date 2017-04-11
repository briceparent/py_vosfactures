from settings import AVAILABLE_COMMANDS
from utils import delete, get, post, put


class ObjectIsDeletedError(Exception):
    pass


class CommandUnavailable(Exception):
    pass


class BaseData:
    _create_data = dict(json_page="", action="")
    _delete_data = dict(json_page="", action="")
    _get_data = dict(json_page="", action="")
    _list_data = dict(json_page="", action="")
    _update_data = dict(json_page="", action="")
    _required_properties = []
    _auto_data = []
    _default_data = []
    _assigning_data = False
    _is_deleted = False
    _forbidden_commands = []

    def _check_command_available(self, command):
        if hasattr(self, "__name__"):
            # Called from a classmethod
            the_class = self
        else:
            # Called from an instance's method
            the_class = self.__class__

        classname = the_class.__name__

        if command in the_class._forbidden_commands:
            raise CommandUnavailable('The "{}" command does not exist for {} model'.format(command, classname))

        if command not in AVAILABLE_COMMANDS[classname]:
            raise CommandUnavailable('The "{}" command is not allowed for {} model'.format(command, classname))

    @classmethod
    def create(cls, **kwargs):
        cls._check_command_available(cls, 'create')

        nothing = object()
        missing_fields = []
        for argument in cls._required_properties:
            if kwargs.get(argument, nothing) == nothing:
                missing_fields.append(argument)

        if missing_fields:
            raise ValueError('Some fields ({}) are required to create this object'.format(", ".join(missing_fields)))

        for argument in cls._default_data:
            if kwargs.get(argument, nothing) == nothing:
                kwargs[argument] = getattr(cls, argument)

        kwargs.update(cls._create_data)
        element_data = post(**kwargs)
        element = cls()
        element._set_data(**element_data)
        return element

    def delete(self):
        self._check_command_available('delete')

        if self._is_deleted:
            raise ObjectIsDeletedError("This object doesn't exist anymore")

        kwargs = dict(instance_id=self.id)
        kwargs.update(self._delete_data)
        delete(**kwargs)
        self._is_deleted = True

    @classmethod
    def get(cls, instance_id):
        cls._check_command_available(cls, 'get')

        kwargs = dict(instance_id=instance_id)
        kwargs.update(cls._get_data)
        element_data = get(**kwargs)
        element = cls()
        element._set_data(id=instance_id)
        element._set_data(**element_data)
        return element

    @classmethod
    def list(cls):
        cls._check_command_available(cls, 'list')

        elements = get(**cls._list_data)
        instances = []
        for element in elements:
            instance = cls()
            instance._set_data(**element)
            instances.append(instance)

        return instances

    def update(self):
        self._check_command_available('update')

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


class Product(BaseData):
    _create_data = dict(json_page="products", action="product")
    _delete_data = dict(json_page="products", action="product")
    _get_data = dict(json_page="products", action="product")
    _list_data = dict(json_page="products", action="products")
    _update_data = dict(json_page="products", action="product")
    _required_properties = ["name", "price_net", "tax"]
    _auto_data = ['created_at', 'updated_at', 'deleted']
    _default_data = ['currency']

    id = None
    name = None
    description = None
    price_net = None
    tax = None
    created_at = None
    updated_at = None
    disabled = None
    deleted = None
    code = None
    currency = 'EUR'
    category_id = None
    kind = None

    def __str__(self):
        return "{} : {} ({} {})".format(self.id, self.name, self.price_net, self.currency)


class Department(BaseData):
    _create_data = dict(json_page="departments", action="departments")
    _delete_data = dict(json_page="departments", action="departments")
    _get_data = dict(json_page="departments", action="department")
    _list_data = dict(json_page="departments", action="departments")
    _update_data = dict(json_page="departments", action="departments")
    _forbidden_commands = ['create', 'update', 'delete']

    id = None
    shortcut = None
    name = None

    def __str__(self):
        return "{} ({})".format(self.name, self.shortcut)


class Invoice(BaseData):
    _create_data = dict(json_page="invoices", action="invoice")
    _delete_data = dict(json_page="invoices", action="invoice")
    _get_data = dict(json_page="invoices", action="invoice")
    _list_data = dict(json_page="invoices", action="invoices")
    _update_data = dict(json_page="invoices", action="invoice")
    _required_properties = ['number', "title", "issue_date", "department_id", "client_id", "positions"]
    _auto_data = ['created_at', 'updated_at']
    _default_data = ['kind']

    id = None
    title = ""  # Objet
    number = None  # "13/2012" - numéro du document (généré automatiquement si non indiqué)
    place = None  # lieu de création
    payment_type = PaymmentType.transfer  # mode de règlement
    price_net = None
    price_gross = None
    currency = "EUR"  # devise
    status = Status.issued  # état du document
    description = None # Informations spécifiques
    paid = "0,00"  # montant payé
    lang = "fr"  # langue du document
    recipient_id = None
    client_id = None
    invoice_id = None
    kind = DocumentKind.bill
    token = None
    cancelled = None
    income = DocumentIncome.income

    payment_to_kind = 31  # date limite de règlement (parmi les options proposées). Si l'option est "Autre" ("other_date"), vous pouvez définir une date spécifique grâce au champ "payment_to". Si vous indiquez "5", la date d'échéance est de 5 jours. Pour ne pas afficher ce champ, indiquez "off".
    sell_date = "off"   # - date additionnelle (ex: date de vente) : date complète ou juste mois et année:YYYY-MM. Pour ne pas faire apparaître cette date, indiquez "off" (ou décochez l'option "Afficher la Date additionnelle" depuis vos paramètres du compte).
    created_at = None
    updated_at = None
    sent_time = None
    paid_date = None  # Date du paiement
    payment_to = None  # date limite de règlement
    issue_date = None  # "2013-01-16" - date de création

    description_footer = ""  # Bas de page
    description_long = ""  # Texte additionnel (imprimé sur la page suivante)
    positions = []  # Liste de positions
    hide_tax = "1"  # Montant TTC uniquement (ne pas afficher de montant HT ni de taxe)
    calculating_strategy = CalculatingStrategy.position

    def __str__(self):
        return "{} : {} ({} {})".format(self.id, self.number, self.price_net, self.currency)

    @classmethod
    def create(cls, **kwargs):
        # For my needs, I want to prevent the  creation of products from the creation of invoices. Products should be
        # created separately then added the new invoices.
        products = kwargs.get("positions", [])
        error = False
        if products:
            for product in products:
                if 'product_id' not in product:
                    # If this keyword is not set, a new product would be generated
                    error = True

        else:
            error = True

        if error:
            raise ValueError("The creation of invoices require existing products")

        return super().create(**kwargs)

    def set_status(self, status):
        self.status = status
        self.update()
